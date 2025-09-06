from devices import Device


class CatFeeder(Device):
    def __init__(self, device_name: str):
        super().__init__(device_type="feeder")
        self.name = device_name