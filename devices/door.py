from enum import Enum, auto
from transitions import Machine
from devices import Device


class DoorState(Enum):
    OPENED = auto()
    CLOSED = auto()
    LOCKED = auto()
    DISCONNECTED = auto()

class Door(Device):

    def on_enter_CLOSED(self):
        print(f'Porta {self.name} fechada')

    def on_enter_OPENED(self):
        print(f"Porta {self.name} aberta")

    def on_enter_LOCKED(self):
        print(f'Porta {self.name} trancada')

    def on_enter_DISCONNECTED(self):
        print(f'Porta {self.name} desconectada')

    def is_OPENED(self):
        return self.state == DoorState.OPENED

    def is_LOCKED(self):
        return self.state == DoorState.LOCKED

    def reconnection(self):
        print(f'Porta {self.name} reconectada')

    def __init__(self, device_name: str):
        super().__init__(device_type="door")
        self.name = device_name
        self.machine = Machine(model=self, states=DoorState, initial=DoorState.CLOSED)

        self.machine.add_transition('open', DoorState.CLOSED, DoorState.OPENED, unless=['is_LOCKED', 'is_DISCONNECTED'])
        self.machine.add_transition('close', DoorState.OPENED, DoorState.CLOSED, unless='is_DISCONNECTED')
        self.machine.add_transition('lock', DoorState.CLOSED, DoorState.LOCKED, unless=['is_OPENED', 'is_DISCONNECTED'])
        self.machine.add_transition('unlock', DoorState.LOCKED, DoorState.CLOSED, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnect', '*', DoorState.DISCONNECTED)
        self.machine.add_transition('reconnect', DoorState.DISCONNECTED, DoorState.CLOSED, after='reconnection')
