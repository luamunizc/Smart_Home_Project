from enum import Enum, auto
from transitions import Machine
from devices import Device, console

class DoorState(Enum):
    OPENED = auto()
    CLOSED = auto()
    LOCKED = auto()
    DISCONNECTED = auto()

class Door(Device):

    def _failed_close(self):

        self.failed_close += 1
        if self.state == DoorState.CLOSED:
            console.print(f"AVISO: A porta '{self.name}' já está fechada!", style='bright_yellow')
        elif self.state == DoorState.LOCKED:
            console.print(f"AVISO: Não é possível fechar a porta '{self.name}' pois ela já está trancada!", style='bright_yellow')

    def _failed_lock(self):

        self.failed_lock += 1
        if self.state == DoorState.OPENED:
            console.print(f"AVISO: Não é possível trancar a porta '{self.name}' pois ela está aberta!", style='bright_red')
        elif self.state == DoorState.LOCKED:
            console.print(f"AVISO: A porta {self.name} já está trancada!", style='bright_yellow')
        print(f"Total de tentativas de trancamento inválidas: {self.failed_lock}")

    def _failed_unlock(self):

        self.failed_unlock += 1
        if self.state == DoorState.OPENED:
            console.print(f"AVISO: Não é possível destrancar a porta '{self.name}' pois ela está aberta!", style='bright_red')
        elif self.state == DoorState.CLOSED:
            console.print(f"AVISO: Não é possível destrancar a porta '{self.name}' pois ela já está destrancada!", style='bright_yellow')
        print(f"Total de tentativas de destrancamento inválidas: {self.failed_unlock}")

    def _failed_open(self):

        self.failed_open += 1
        if self.state == DoorState.LOCKED:
            console.print(f"AVISO: Não é possível abrir a porta '{self.name}' pois ela está trancada!", style='bright_red')
        elif self.state == DoorState.OPENED:
            console.print(f"AVISO: A porta '{self.name}' já está aberta!", style='bright_yellow')
        print(f"Total de tentativas de abertura inválidas: {self.failed_open}")

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

    def reconnection_fail(self):
        console.print(f"A porta {self.name} já está conectada", style='bright_magenta')

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="door")
        self.failed_close = 0
        self.failed_lock = 0
        self.failed_open = 0
        self.failed_unlock = 0
        self.machine = Machine(model=self, states=DoorState, initial=DoorState.CLOSED)

        self.machine.add_transition('open', DoorState.CLOSED, DoorState.OPENED, unless=['is_LOCKED', 'is_DISCONNECTED'])
        self.machine.add_transition('close', DoorState.OPENED, DoorState.CLOSED, unless='is_DISCONNECTED')
        self.machine.add_transition('lock', DoorState.CLOSED, DoorState.LOCKED, unless=['is_OPENED', 'is_DISCONNECTED'])
        self.machine.add_transition('unlock', DoorState.LOCKED, DoorState.CLOSED, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnect', '*', DoorState.DISCONNECTED)
        self.machine.add_transition('reconnect', DoorState.DISCONNECTED, DoorState.CLOSED, after='reconnection')
        self.machine.add_transition('lock', DoorState.OPENED, '=', after='_failed_lock', unless='is_DISCONNECTED')
        self.machine.add_transition('lock', DoorState.LOCKED, '=', after='_failed_lock', unless='is_DISCONNECTED')
        self.machine.add_transition('open', DoorState.LOCKED, '=', after='_failed_open', unless='is_DISCONNECTED')
        self.machine.add_transition('open', DoorState.OPENED, '=', after='_failed_open', unless='is_DISCONNECTED')
        self.machine.add_transition('unlock', DoorState.OPENED, '=', after='_failed_unlock', unless='is_DISCONNECTED')
        self.machine.add_transition('unlock', DoorState.CLOSED, '=', after='_failed_unlock', unless='is_DISCONNECTED')
        self.machine.add_transition('reconnect', [DoorState.CLOSED, DoorState.OPENED, DoorState.LOCKED], '=', after='reconnection_fail')
        self.machine.add_transition('close', DoorState.CLOSED, '=', after='_failed_close', unless='is_DISCONNECTED')
        self.machine.add_transition('close', DoorState.LOCKED, '=', after='_failed_close', unless='is_DISCONNECTED')


if __name__ == '__main__':
    d = Door("door")
    d.open()
    d.unlock()
    d.close()
    d.close()
    d.unlock()