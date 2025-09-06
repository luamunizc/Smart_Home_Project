from enum import Enum, auto
from transitions import Machine
from devices import Device


class AlarmState(Enum):
    ACTIVATED = auto()
    DEACTIVATED = auto()
    RINGING = auto()
    ALERT = auto()

class Alarm(Device):

    def on_ACTIVATED(self):
        print("Alarm activated")

    def on_RINGING(self):
        print('UIOO UIOO UIOO UIOO')
        # Precisaria de uma coisa pra enviar msg pra pessoa

    def __init__(self, device_name: str):
        super().__init__(device_type="alarm")
        self.name = device_name
        self.machine = Machine(model=self, states=AlarmState, initial=AlarmState.DEACTIVATED)

        self.machine.add_transition('activate', AlarmState.DEACTIVATED, AlarmState.ACTIVATED)
        self.machine.add_transition('ring', AlarmState.ACTIVATED, AlarmState.RINGING)
        self.machine.add_transition('stop', AlarmState.RINGING, AlarmState.ALERT)
        self.machine.add_transition('rest', AlarmState.ALERT, AlarmState.ACTIVATED)
        self.machine.add_transition('deactivate', '*', AlarmState.DEACTIVATED)