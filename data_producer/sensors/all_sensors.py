from datetime import datetime
import random
from pathlib import Path
import json

from sensors.base_sensor import BaseSensor


class TemperatureSensor(BaseSensor):
    def __init__(self, room, unit, device_type, min_value, max_value):
        super().__init__(room, unit, device_type, min_value, max_value)


class HumiditySensor(BaseSensor):
    def __init__(self, room, unit, device_type, min_value, max_value):
        super().__init__(room, unit, device_type, min_value, max_value)


class ElectricitySensor(BaseSensor):

    def __init__(self, room, unit, device_type):
        super().__init__(room, unit, device_type, min_value=None, max_value=None)
        self.state_elec_file = Path(f"/app/states/elec_sensor_{room}.json")
        self.current_value = self.load_state()

    def load_state(self):
        if self.state_elec_file.exists():
            with open(self.state_elec_file, 'r') as f:
                state = json.load(f)
                return state.get('elec_value', 1000.0)
        return 1000.0
    
    def write_state(self):
        with open(self.state_elec_file, 'w') as f:
            json.dump({'elec_value': self.current_value}, f)

    def get_value(self):
        increment = round(random.uniform(0.2, 2.0), 1)
        self.current_value = round(self.current_value + increment, 1)
        self.write_state()
        return self.current_value


class WaterSensor(BaseSensor):
    def __init__(self, room, unit, device_type):
        super().__init__(room, unit, device_type, min_value=None, max_value=None)
        self.state_water_file = Path(f"/app/states/water_sensor_{room}.json")
        self.current_value = self.load_state()

    def load_state(self):
        if self.state_water_file.exists():
            with open(self.state_water_file, 'r') as f:
                state = json.load(f)
                return state.get('water_value', 1000.0) # если нет ключа, вернет значение 1000.0
        return 1000.0
    
    def write_state(self):
        with open(self.state_water_file, 'w') as f:
            json.dump({'water_value': self.current_value}, f)

    def get_value(self):
        increment = round(random.uniform(0.0, 0.5), 1)
        self.current_value = round(self.current_value + increment, 1)
        self.write_state()
        return self.current_value