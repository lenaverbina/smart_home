import aio_pika

import asyncio
import os
import json
from producer.generate_sensors import sensors

"""
Скрипт, который генерирует словарь вида - данные с датчика
{
    "timestamp": "2026-03-03T11:04:04.221723", - время отправки данных с датчика, ISO формат
    "device_id": "temperature_sensor_living_room", - 
    "device_type": "temperature",  # или humidity, light, water, electricity
    "value": 23.5,
    "unit": "celsius",
    "room": "living_room"
}

room : [kitchen, living_room, bedroom, bathroom]
device_type : [temperature, humidity, water, electricity]
"device_id" : [temp|humidity|water|electricity]
"""
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))


async def send_sensor(sensor, channel):
    data = sensor.produce_data()
    message = aio_pika.Message(
        body=json.dumps(data).encode(),
        delivery_mode=2
    )
    
    await channel.default_exchange.publish(
        message,
        routing_key='sensor_data'
    )

async def send_all_sensors(sensors):
    """
    Устанавливаем одно соединение на всю процедуру запихивания сообщений в очередь rabbitmq
    """
    connection = await aio_pika.connect(
        host=rabbitmq_host,
        port=rabbitmq_port
    )

    async with connection:
        channel = await connection.channel()

        await channel.declare_queue(
            'sensor_data', 
            durable=True
        )

        await asyncio.gather(*[
            send_sensor(sensor, channel) 
            for sensor in sensors
        ])

if __name__ == "__main__":
    asyncio.run(send_all_sensors(sensors))
