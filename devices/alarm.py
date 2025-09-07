from threading import Timer
from enum import Enum, auto
from transitions import Machine
from devices import Device


class AlarmState(Enum):
    ACTIVATED = auto()
    DEACTIVATED = auto()
    RINGING = auto()
    ALERT = auto()
    DISCONNECTED = auto()

class Alarm(Device):

    def _send_notification(self, message: str):
        print(f"📢 NOTIFICAÇÃO: {message}")

    def on_enter_ACTIVATED(self):
        print(f"Alarme {self.name} está ativado")

    def on_enter_RINGING(self):
        print('🚨UIOO🚨UIOO🚨UIOO🚨UIOO🚨') # Alarme apitando
        self._send_notification(f"ALERTA! O alarme '{self.name}' foi disparado!")

    def on_enter_ALERT(self):
        print(f"Alarme {self.name} está em modo de alerta")

    def is_DISCONNECTED(self):
        return self.state == AlarmState.DISCONNECTED

    # Não irei salvar o modo antes da desconexão pois acho que seria melhor para a segurança reconectar em modo alerta

    def alert_timer(self):
        t = Timer(120.0, self.rest)
        t.start()

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="alarm")
        self.name = device_name
        self.machine = Machine(model=self, states=AlarmState, initial=AlarmState.DEACTIVATED)

        self.machine.add_transition('activate', AlarmState.DEACTIVATED, AlarmState.ACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('ring', AlarmState.ACTIVATED, AlarmState.RINGING, unless='is_DISCONNECTED')
        self.machine.add_transition('stop', AlarmState.RINGING, AlarmState.ALERT, unless='is_DISCONNECTED')
        self.machine.add_transition('rest', AlarmState.ALERT, AlarmState.ACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('deactivate', '*', AlarmState.DEACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnection', '*', AlarmState.DISCONNECTED)
        self.machine.add_transition('reconnect', AlarmState.DISCONNECTED, AlarmState.ALERT, after='alert_timer')