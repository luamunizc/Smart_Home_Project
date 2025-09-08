from threading import Timer
from enum import Enum, auto
from transitions import Machine
from central.devices.devices import Device, console


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
        print(f"Alarme '{self.name}' está ativado")

    def on_enter_RINGING(self):
        print('🚨UIOO🚨UIOO🚨UIOO🚨UIOO🚨') # Alarme apitando
        self._send_notification(f"ALERTA! O alarme '{self.name}' foi disparado!")

    def on_enter_ALERT(self):
        print(f"Alarme '{self.name}' está em modo de alerta")

    def is_DISCONNECTED(self):
        return self.state == AlarmState.DISCONNECTED

    def activate_fail(self):
        if self.state == AlarmState.ACTIVATED:
            console.print(f"Alarme '{self.name}' já está ativado!", style='bright_yellow')
        elif self.state == AlarmState.ALERT or self.state == AlarmState.RINGING:
            console.print(f"O alarme '{self.name}' saiu do estado de alerta mas continua ativado!", style='bright_cyan')
        elif self.state == AlarmState.DISCONNECTED:
            console.print(f"Reconecte o alarme '{self.name}' antes de ativar!")

    def failed_stop(self):
        if self.state == AlarmState.ACTIVATED:
            console.print(f"O alarme '{self.name}' nao está apitando para precisar parar")
        elif self.state == AlarmState.ALERT:
            console.print(f"O alarme '{self.name}' já parou de apitar")
        elif self.state == AlarmState.RINGING:
            console.print(f"O alarme '{self.name}' está desativado!", style='bold yellow')
        elif self.state == AlarmState.DISCONNECTED:
            console.print(f"O ALARME '{self.name.upper()}' ESTA DESCONECTADO!", style='bold bright_red')

    def on_enter_DISCONNECTED(self):
        console.print(f"ATENCAO! O ALARME '{self.name.upper()}' ESTA DESCONECTADO!", style='bold bright_red')

    # Não irei salvar o modo antes da desconexão pois acho que seria melhor para a segurança reconectar em modo alerta

    def on_exit_DISCONNECTED(self):
        t = Timer(120.0, self.rest)
        t.start()

    def already_connected(self):
        console.print(f"O alarme '{self.name}' já esta conectado!", style='green')

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="alarm")
        self.name = device_name
        self.machine = Machine(model=self, states=AlarmState, initial=AlarmState.DEACTIVATED)

        self.machine.add_transition('activate', AlarmState.DEACTIVATED, AlarmState.ACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('activate', [AlarmState.RINGING, AlarmState.ALERT, AlarmState.ACTIVATED, AlarmState.DISCONNECTED, AlarmState.ACTIVATED], '=', after='activate_fail')
        self.machine.add_transition('ring', AlarmState.ACTIVATED, AlarmState.RINGING, unless='is_DISCONNECTED')
        self.machine.add_transition('stop', AlarmState.RINGING, AlarmState.ALERT, unless='is_DISCONNECTED')
        self.machine.add_transition('stop', [AlarmState.ACTIVATED, AlarmState.ALERT, AlarmState.DEACTIVATED, AlarmState.DISCONNECTED], '=', after='failed_stop')
        self.machine.add_transition('rest', AlarmState.ALERT, AlarmState.ACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('deactivate', '*', AlarmState.DEACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnection', '*', AlarmState.DISCONNECTED)
        self.machine.add_transition('reconnect', AlarmState.DISCONNECTED, AlarmState.ALERT)
        self.machine.add_transition('reconnect', [AlarmState.ACTIVATED, AlarmState.DEACTIVATED, AlarmState.RINGING, AlarmState.ALERT], '=', after='already_connected')

if __name__ == "__main__":
    s = Alarm('Principal')
    s.activate()
    s.stop()
    # s.activate()
    # s.reconnect()
    s.disconnection()
    s.stop()