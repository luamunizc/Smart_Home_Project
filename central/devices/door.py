from enum import Enum, auto
from transitions import Machine
from devices.devices import Device, console

class DoorState(Enum):
    ABERTA = auto()
    FECHADA = auto()
    TRANCADA = auto()
    DESCONECTADA = auto()

class Door(Device):

    def _failed_close(self):

        self.failed_close += 1
        if self.state == DoorState.FECHADA:
            self.notificar(f"AVISO: A porta '{self.name}' já está fechada!")
        elif self.state == DoorState.TRANCADA:
            self.notificar(f"AVISO: Não é possível fechar a porta '{self.name}' pois ela já está trancada!")

    def _failed_lock(self):

        self.failed_lock += 1
        if self.state == DoorState.ABERTA:
            self.notificar(f"AVISO: Não é possível trancar a porta '{self.name}' pois ela está aberta!")
        elif self.state == DoorState.TRANCADA:
            self.notificar(f"AVISO: A porta {self.name} já está trancada!")
        self.notificar(f"Total de tentativas de trancamento inválidas: {self.failed_lock}")

    def _failed_unlock(self):

        self.failed_unlock += 1
        if self.state == DoorState.ABERTA:
            self.notificar(f"AVISO: Não é possível destrancar a porta '{self.name}' pois ela está aberta!")
        elif self.state == DoorState.FECHADA:
            self.notificar(f"AVISO: Não é possível destrancar a porta '{self.name}' pois ela já está destrancada!")
        self.notificar(f"Total de tentativas de destrancamento inválidas: {self.failed_unlock}")

    def _failed_open(self):

        self.failed_open += 1
        if self.state == DoorState.TRANCADA:
            self.notificar(f"AVISO: Não é possível abrir a porta '{self.name}' pois ela está trancada!")
        elif self.state == DoorState.ABERTA:
            self.notificar(f"AVISO: A porta '{self.name}' já está aberta!")
        self.notificar(f"Total de tentativas de abertura inválidas: {self.failed_open}")

    def on_enter_FECHADA(self):
        self.notificar(f'Porta {self.name} fechada')

    def on_enter_ABERTA(self):
        self.notificar(f"Porta {self.name} aberta")

    def on_enter_TRANCADA(self):
        self.notificar(f'Porta {self.name} trancada')

    def on_enter_DESCONECTADA(self):
        self.notificar(f'Porta {self.name} desconectada')

    def is_ABERTA(self):
        return self.state == DoorState.ABERTA

    def is_TRANCADA(self):
        return self.state == DoorState.TRANCADA

    def reconnection(self):
        self.notificar(f'Porta {self.name} reconectada')

    def reconnection_fail(self):
        self.notificar(f"A porta {self.name} já está conectada")

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="porta")
        self.failed_close = 0
        self.failed_lock = 0
        self.failed_open = 0
        self.failed_unlock = 0
        self.machine = Machine(model=self, states=DoorState, initial=DoorState.FECHADA, after_state_change="notificar")

        self.machine.add_transition('open', DoorState.FECHADA, DoorState.ABERTA, unless=['is_TRANCADA', 'is_DESCONECTADA'])
        self.machine.add_transition('close', DoorState.ABERTA, DoorState.FECHADA, unless='is_DESCONECTADA')
        self.machine.add_transition('lock', DoorState.FECHADA, DoorState.TRANCADA, unless=['is_ABERTA', 'is_DESCONECTADA'])
        self.machine.add_transition('unlock', DoorState.TRANCADA, DoorState.FECHADA, unless='is_DESCONECTADA')
        self.machine.add_transition('disconnect', '*', DoorState.DESCONECTADA)
        self.machine.add_transition('reconnect', DoorState.DESCONECTADA, DoorState.FECHADA, after='reconnection')
        self.machine.add_transition('lock', DoorState.ABERTA, '=', after='_failed_lock', unless='is_DESCONECTADA')
        self.machine.add_transition('lock', DoorState.TRANCADA, '=', after='_failed_lock', unless='is_DESCONECTADA')
        self.machine.add_transition('open', DoorState.TRANCADA, '=', after='_failed_open', unless='is_DESCONECTADA')
        self.machine.add_transition('open', DoorState.ABERTA, '=', after='_failed_open', unless='is_DESCONECTADA')
        self.machine.add_transition('unlock', DoorState.ABERTA, '=', after='_failed_unlock', unless='is_DESCONECTADA')
        self.machine.add_transition('unlock', DoorState.FECHADA, '=', after='_failed_unlock', unless='is_DESCONECTADA')
        self.machine.add_transition('reconnect', [DoorState.FECHADA, DoorState.ABERTA, DoorState.TRANCADA], '=', after='reconnection_fail')
        self.machine.add_transition('close', DoorState.FECHADA, '=', after='_failed_close', unless='is_DESCONECTADA')
        self.machine.add_transition('close', DoorState.TRANCADA, '=', after='_failed_close', unless='is_DESCONECTADA')



if __name__ == '__main__':
    d = Door("porta")
    d.notificar()
    d.open()
    d.unlock()
    d.close()
    d.close()
    d.unlock()