from devices import Device


class Lamp(Device):
    def __init__(self, device_name: str):
        super().__init__(device_type="lamp")
        self.name = device_name
