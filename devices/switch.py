from enum import Enum
from transitions import Machine
from devices import Device


class SwitchState(Enum):
    OFF = 0
    ON = 1

class Switch(Device):
    def __init__(self):
        super().__init__()
        self.machine = Machine(model=self, states=SwitchState, initial=SwitchState.OFF)

        self.machine.add_transition('ligar', SwitchState.OFF, SwitchState.ON)
        self.machine.add_transition('desligar', SwitchState.ON, SwitchState.OFF)


if __name__ == "__main__":
    s = Switch()
    print(s.state)
    s.ligar()
    print(s.state)