from rich.console import Console

console = Console()

class Device:
    def __init__(self, device_type: str, device_name: str):
        self.name = device_name
        self.type = device_type


    def to_dict(self):
        return {'name': self.name, 'type': self.type, 'state': self.state.value}

    def __str__(self):
        return f"Dispositivo {self.name} do tipo {self.type} no estado {self.state.name}"