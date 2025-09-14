from enum import Enum, auto
from transitions import Machine
from threading import Timer
from devices.devices import Device, console
from random import randrange
from time import sleep


class FeederState(Enum):
    EMPTY = auto()
    IDLE = auto()
    FEEDING = auto()
    DISCONNECTED = auto()

class Feeder(Device):

    def is_EMPTY(self):
        return self.level < 5.2

    def is_DISCONNECTED(self):
        return self.state == FeederState.DISCONNECTED

    def refilled(self):
        console.print(f"Alimentador '{self.name}' reabastecido", style='bright_green')
        self.level = 100 # Assumindo um reabastecimento de 100%

    def on_enter_IDLE(self):
        console.print(f"Alimentador '{self.name}' em modo standby")

    def on_enter_FEEDING(self):
        console.print(f"Alimentador '{self.name}' enchendo o pote de racao", style="dark_goldenrod")

    def on_enter_EMPTY(self):
        console.print(f"Alimentador '{self.name}' precisa ser recarregado!", style='red')

    def start_feeding(self):
        drop = 4 + (randrange(80, 120) / 100) # Adicionando um pouco de variação ao processo
        self.level -= drop
        console.print(f"Nível de ração atual: {self.level:.1f}%", style='bright_magenta')
        timer = Timer(1.0, self.stop)
        timer.start()

    def finish_feeding(self):
        if self.is_EMPTY():
            self.empty()
        elif self.level < 20:
            console.print(f"AVISO: Alimentador '{self.name}' está com pouca ração ({self.level:.1f}%)!", style='orange1')

    def feeding_empty(self):
        console.print(f"O alimentador '{self.name}' está vazio! Reabasteca antes de usar.", style='bold bright_red')

    def empty_reconnection(self):
        if self.is_EMPTY():
            self.empty()

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="feeder")
        self.level = 0
        self.machine = Machine(model=self, states=FeederState, initial=FeederState.EMPTY)
        self.machine.add_transition('refill', FeederState.EMPTY, FeederState.IDLE, before='refilled')
        self.machine.add_transition('feed', FeederState.IDLE, FeederState.FEEDING, unless=['is_DISCONNECTED', 'is_EMPTY'], after='start_feeding')
        self.machine.add_transition('stop', FeederState.FEEDING, FeederState.IDLE, unless='is_DISCONNECTED', after='finish_feeding')
        self.machine.add_transition('empty', FeederState.IDLE, FeederState.EMPTY, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnect', '*', FeederState.DISCONNECTED)
        self.machine.add_transition('reconnect', FeederState.DISCONNECTED, FeederState.IDLE, after='empty_reconnection')
        self.machine.add_transition('feed', FeederState.EMPTY, FeederState.EMPTY, after='feeding_empty')


# teste
if __name__ == "__main__":
    cf = Feeder('malelo')
    cf.refill()
    for _ in range(21):
        cf.feed()
        sleep(1.5)

