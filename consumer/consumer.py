import pika
import pandas as pd
from clickhouse_driver import Client


import os
import json
from datetime import datetime
import uuid

"""
консьюмер, который забирает сообщения из rabbitmq синхронно и отдает на обработку в spark
"""

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))

client = Client(host='clickhouse', port=9000, user='default', password='default')

client.execute('CREATE DATABASE IF NOT EXISTS smart_home')

client.execute('''
    CREATE TABLE IF NOT EXISTS smart_home.sensor_readings_2 (
        device_id String,
        timestamp DateTime64(6),
        value Float32,
        unit String,
        room String,
        device_type String
        ) ENGINE = MergeTree()
        ORDER BY (device_id, timestamp)
    ''')

def consume():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port)
    ) # блокирующее соединение
    channel = connection.channel() # создаем отдельный канал для того, чтобы забирать сообщения
    BATCH_SIZE = 100
    total_processed = 0

    while True:
        messages = []
        for _ in range(BATCH_SIZE):
            method, properties, body = channel.basic_get('sensor_data') 
            if not method:
                break # выходим из цикла, если нет сообщений
            messages.append((method, json.loads(body)))

        if not messages:
            break

        try:
            send_to_spark([m[1] for m in messages]) # отправляем в Spark пакетом 
        except Exception as e:
            print(f"Ошибка при отправке в Spark: {e}")
            raise
        else:
            for method, body in messages:
                channel.basic_ack(method.delivery_tag) # удаляем сообщение из очереди, если удалось создать файл формата паркет

        total_processed += len(messages)
        print(f"Обработано {total_processed} сообщений")

    print(f"✅ Готово, всего {total_processed}")
    connection.close()

def send_to_spark(messages):
    df = pd.DataFrame(messages)
    now = datetime.now()
    batch_id = str(uuid.uuid4())[:8]
    filename = f"/app/data/batch_sensor_data_{now.strftime('%Y%m%d_%H%M%S_%f')}_{batch_id}.parquet"
    df.to_parquet(filename)

if __name__ == "__main__":
    consume()