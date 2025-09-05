from enum import Enum, auto
from transitions import Machine
from devices import Device


class AlarmState(Enum):
    ACTIVATED = auto()
    DEACTIVATED = auto()
    RINGING = auto()
    ALERT = auto()

class Alarm(Device):
    def __init__(self):
        super().__init__()
        self.machine = Machine(model=self, states=AlarmState, initial=AlarmState.DEACTIVATED)

        self.machine.add_transition('activate', AlarmState.DEACTIVATED, AlarmState.ACTIVATED)
        self.machine.add_transition('ring', AlarmState.ACTIVATED, AlarmState.RINGING)
        self.machine.add_transition('stop', AlarmState.RINGING, AlarmState.ALERT)
        self.machine.add_transition('rest', AlarmState.ALERT, AlarmState.ACTIVATED)
        self.machine.add_transition('deactivate', AlarmState.ACTIVATED, AlarmState.DEACTIVATED)