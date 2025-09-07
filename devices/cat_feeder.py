from enum import Enum, auto
from transitions import Machine
from threading import Timer
from devices import Device


class CatFeederState(Enum):
    EMPTY = auto()
    IDLE = auto()
    FEEDING = auto()
    DISCONNECTED = auto()

class CatFeeder(Device):

    def is_EMPTY(self):
        return self.level < 10

    def is_DISCONNECTED(self):
        return self.state == CatFeederState.DISCONNECTED

    def refilled(self):
        print(f"Alimentador {self.name} reabastecido")
        self.level = 100 # Assumindo um reabastecimento de 100%

    def on_enter_IDLE(self):
        print(f"Alimentador {self.name} em modo standby")

    def on_enter_FEEDING(self):
        print(f"Alimentador {self.name} enchendo o pote de racao")

    def on_enter_EMPTY(self):
        print(f"Alimentador {self.name} precisa ser recarregado!")

    def start_feeding(self):
        self.level -= 5
        print(f"Nível de ração atual: {self.level}%")
        timer = Timer(10.0, self.stop())
        timer.start()

    def finish_feeding(self):
        if self.is_EMPTY():
            self.empty()
        elif self.level < 25:
            print(f" AVISO: Alimentador '{self.name}' está com pouca ração ({self.level}%)!")

    def empty_reconnection(self):
        if self.is_EMPTY():
            self.empty()

    def __init__(self, device_name: str):
        super().__init__(device_type="feeder")
        self.name = device_name
        self.level = 0
        self.machine = Machine(model=self, states=CatFeederState, initial=CatFeederState.EMPTY)
        self.machine.add_transition('refill', CatFeederState.EMPTY, CatFeederState.IDLE, before='refilled')
        self.machine.add_transition('feed', CatFeederState.IDLE, CatFeederState.FEEDING, unless=['is_DISCONNECTED', 'is_EMPTY'], after='start_feeding')
        self.machine.add_transition('stop', CatFeederState.FEEDING, CatFeederState.IDLE, unless='is_DISCONNECTED', after='finish_feeding')
        self.machine.add_transition('empty', CatFeederState.IDLE, CatFeederState.EMPTY, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnected', '*', CatFeederState.DISCONNECTED)
        self.machine.add_transition('reconnect', CatFeederState.DISCONNECTED, CatFeederState.IDLE, after='empty_reconnection')
