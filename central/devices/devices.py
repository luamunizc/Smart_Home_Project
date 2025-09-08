from rich.console import Console

console = Console()

class Device:
    def __init__(self, device_type: str, device_name: str):
        self.name = device_name
        self.type = device_type
        if self.name == '':
            self.name = f"new_{device_type}"