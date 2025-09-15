from enum import Enum, auto
from transitions import Machine
from threading import Timer
from devices.devices import Device, console
from random import randrange
from time import sleep


class FeederState(Enum):
    VAZIO = auto()
    LIGADO = auto()
    ALIMENTANDO = auto()
    DESCONECTADO = auto()

class Feeder(Device):

    def is_VAZIO(self):
        return self.level < 5.2

    def is_DESCONECTADO(self):
        return self.state == FeederState.DESCONECTADO

    def refilled(self):
        console.print(f"Alimentador '{self.name}' reabastecido", style='bright_green')
        self.level = 100 # Assumindo um reabastecimento de 100%

    def on_enter_LIGADO(self):
        console.print(f"Alimentador '{self.name}' em modo standby")

    def on_enter_ALIMENTANDO(self):
        console.print(f"Alimentador '{self.name}' enchendo o pote de racao", style="dark_goldenrod")

    def on_enter_VAZIO(self):
        console.print(f"Alimentador '{self.name}' precisa ser recarregado!", style='red')

    def start_feeding(self):
        drop = 4 + (randrange(80, 120) / 100) # Adicionando um pouco de variação ao processo
        self.level -= drop
        console.print(f"Nível de ração atual: {self.level:.1f}%", style='bright_magenta')
        timer = Timer(1.0, self.stop)
        timer.start()

    def finish_feeding(self):
        if self.is_VAZIO():
            self.empty()
        elif self.level < 20:
            console.print(f"AVISO: Alimentador '{self.name}' está com pouca ração ({self.level:.1f}%)!", style='orange1')

    def feeding_empty(self):
        console.print(f"O alimentador '{self.name}' está vazio! Reabasteca antes de usar.", style='bold bright_red')

    def empty_reconnection(self):
        if self.is_VAZIO():
            self.empty()

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="feeder")
        self.level = 0
        self.machine = Machine(model=self, states=FeederState, initial=FeederState.VAZIO)
        self.machine.add_transition('refill', [FeederState.VAZIO, FeederState.LIGADO], FeederState.LIGADO, before='refilled')
        self.machine.add_transition('refill', [FeederState.ALIMENTANDO, FeederState.DESCONECTADO], '=')
        self.machine.add_transition('feed', FeederState.LIGADO, FeederState.ALIMENTANDO, unless=['is_DESCONECTADO', 'is_VAZIO'], after='start_feeding')
        self.machine.add_transition('feed', [FeederState.ALIMENTANDO, FeederState.DESCONECTADO], '=')
        self.machine.add_transition('feed', FeederState.VAZIO, FeederState.VAZIO, after='feeding_empty')
        self.machine.add_transition('stop', FeederState.ALIMENTANDO, FeederState.LIGADO, unless='is_DESCONECTADO', after='finish_feeding')
        self.machine.add_transition('stop', [FeederState.VAZIO, FeederState.LIGADO, FeederState.DESCONECTADO], '=')
        self.machine.add_transition('empty', FeederState.LIGADO, FeederState.VAZIO, unless='is_DESCONECTADO')
        self.machine.add_transition('empty', [FeederState.VAZIO, FeederState.ALIMENTANDO, FeederState.DESCONECTADO], '=')
        self.machine.add_transition('disconnect', '*', FeederState.DESCONECTADO)
        self.machine.add_transition('reconnect', FeederState.DESCONECTADO, FeederState.LIGADO, after='empty_reconnection')
        self.machine.add_transition('reconnect', [FeederState.VAZIO, FeederState.ALIMENTANDO, FeederState.LIGADO], '=')

    def to_dict(self):
        return {'name': self.name, 'type': self.type, 'state': self.state.value, 'level': self.level}

    def __str__(self):
        if self.state == FeederState.VAZIO:
            return f"Alimentador de racao {self.name} vazio"
        else:
            return f"Alimentador de racao {self.name} no estado {self.state.name} e nivel de racao {self.level}"


# teste
if __name__ == "__main__":
    cf = Feeder('malelo')
    cf.refill()
    for _ in range(21):
        cf.feed()
        sleep(1.5)

