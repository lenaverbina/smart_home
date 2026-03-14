from datetime import datetime
import random


class BaseSensor:
    def __init__(self, room, unit, device_type, min_value, max_value):
        self.device_type = device_type
        self.room = room # комната
        self.unit = unit # единица измерения
        self.min_value = min_value # минимальное значение датчика
        self.max_value = max_value # максимальное значение датчика

    def get_value(self):
        """
        Генерируем значение датчика
        """
        value = round(random.uniform(self.min_value, self.max_value), 1)
        return value

    def produce_data(self):
        """
        Генерируем словарь метаданных
        """
        data = {
        'timestamp': datetime.now().isoformat(),  # свежее время
        'room': self.room,
        'unit': self.unit,
        'device_type': self.device_type,
        'device_id': f"{self.device_type}_sensor_{self.room}",
        'value': self.get_value()
        }
        return data