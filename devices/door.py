from enum import Enum, auto
from transitions import Machine
from devices import Device


class DoorState(Enum):
    OPENED = auto()
    CLOSED = auto()
    LOCKED = auto()

class Door(Device):
    def __init__(self, device_name: str):
        super().__init__(device_type="door")
        self.name = device_name
        self.machine = Machine(model=self, states=DoorState, initial=DoorState.CLOSED)

        self.machine.add_transition('open', DoorState.CLOSED, DoorState.OPENED)
        self.machine.add_transition('close', DoorState.OPENED, DoorState.CLOSED)
        self.machine.add_transition('lock', DoorState.CLOSED, DoorState.LOCKED)
        self.machine.add_transition('unlock', DoorState.LOCKED, DoorState.CLOSED)
