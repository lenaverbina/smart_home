from sensors.all_sensors import TemperatureSensor, HumiditySensor, ElectricitySensor, WaterSensor

"""
Водные счетчики только в ванной и на кухне
"""

def create_sensors():
    sensors = []
    rooms = ["bedroom", "kitchen", "living_room", "bathroom"]
    for room in rooms:
        for i in range(100):

            room_id = f"{room}_{i}"
            min_temp = 18.0 if room in ["bedroom", "living_room"] else 20.0
            max_temp = 24.0 if room in ["bedroom", "living_room"] else 26.0

            min_hum = 20.0
            max_hum = 80.0

            sensors.append(
                TemperatureSensor(
                    room=room_id,
                    unit="celsius",
                    device_type="temperature",
                    min_value=min_temp,
                    max_value=max_temp
                )
            )

            if room == "kitchen":
                min_hum = 40.0
                sensors.append(
                WaterSensor(
                    room=room_id,
                    unit="cubic_meter",
                    device_type="water"
                    )
                )
                
            elif room == "bathroom":
                min_hum = 50.0
                sensors.append(
                WaterSensor(
                    room=room_id,
                    unit="cubic_meter",
                    device_type="water"
                    )
                )

            sensors.append(
                HumiditySensor(
                    room=room_id,
                    unit="%",
                    device_type="humidity",
                    min_value=min_hum,
                    max_value=max_hum
                    )
                )
            
            sensors.append(
                ElectricitySensor(
                    room=room_id,
                    unit="kWh",
                    device_type="electricity"
                )
            )
    return sensors

sensors = create_sensors()
