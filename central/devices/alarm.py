from threading import Timer
from enum import Enum, auto
from transitions import Machine
from devices.devices import Device, console
from datetime import datetime


class AlarmState(Enum):
    ACTIVATED = auto()
    DEACTIVATED = auto()
    RINGING = auto()
    ALERT = auto()
    DISCONNECTED = auto()

class Alarm(Device):

    def _send_notification(self, message: str):
        print(f"{datetime.today()} NOTIFICAÇÃO: {message}")

    def on_enter_ACTIVATED(self):
        print(f"Alarme '{self.name}' esta ativado")

    def on_enter_RINGING(self):
        print('🚨UIOO🚨UIOO🚨UIOO🚨UIOO🚨') # Alarme apitando
        self._send_notification(f"ALERTA! O alarme '{self.name}' foi disparado!")
        # t = Timer(120.0, self.stop) # Timer para simular um tempo em que o alarme vai fazer barulho, mas para a entrega desse trabalho, pode ficar sem executar msm
        # t.start()

    def on_enter_ALERT(self):
        print(f"Alarme '{self.name}' está em modo de alerta")
        # t = Timer(120.0, self.rest) # Timer para sair automaticamente do modo alerta
        # t.start()

    def is_DISCONNECTED(self):
        return self.state == AlarmState.DISCONNECTED

    def activate_fail(self):
        if self.state == AlarmState.ACTIVATED:
            console.print(f"Alarme '{self.name}' ja está ativado!", style='bright_yellow')
        elif self.state == AlarmState.ALERT or self.state == AlarmState.RINGING:
            console.print(f"O alarme '{self.name}' saiu do estado de alerta mas continua ativado!", style='bright_cyan')
        elif self.state == AlarmState.DISCONNECTED:
            console.print(f"Reconecte o alarme '{self.name}' antes de ativar!")

    def stop_fail(self):
        if self.state == AlarmState.ACTIVATED:
            console.print(f"O alarme '{self.name}' nao está apitando para precisar parar")
        elif self.state == AlarmState.ALERT:
            console.print(f"O alarme '{self.name}' ja parou de apitar")
        elif self.state == AlarmState.DEACTIVATED:
            console.print(f"O alarme '{self.name}' esta desativado!", style='bold yellow')
        elif self.state == AlarmState.DISCONNECTED:
            console.print(f"O ALARME '{self.name.upper()}' ESTA DESCONECTADO!", style='bold bright_red')

    def ring_fail(self):
        if self.state == AlarmState.DEACTIVATED:
            console.print(f"O alarme '{self.name}' esta desativado!", style='bold yellow')
        elif self.state == AlarmState.DISCONNECTED:
            console.print(f"O alarme '{self.name}' esta desconectado!", style='bold bright_red')

    def rest_fail(self):
        if self.state == AlarmState.DEACTIVATED:
            console.print(f"O alarme '{self.name}' esta desativado!", style='bold yellow')
        elif self.state == AlarmState.DISCONNECTED:
            console.print(f"O alarme '{self.name}' esta desconectado!", style='bold bright_red')
        elif self.state == AlarmState.ACTIVATED:
            console.print(f"O alarme {self.name} nao estava em alerta.", style='bold yellow')

    def deactivate_fail(self):
        if self.state == AlarmState.DEACTIVATED:
            console.print(f"O alarme '{self.name}' ja está desativado.", style='bold yellow')
        elif self.state == AlarmState.DISCONNECTED:
            console.print(f"O ALARME '{self.name.upper()}' ESTA DESCONECTADO!", style='bold bright_red')

    def on_enter_DISCONNECTED(self):
        console.print(f"ATENCAO! O ALARME '{self.name.upper()}' ESTA DESCONECTADO!", style='bold bright_red')

    # Não irei salvar o modo antes da desconexão pois acho que seria melhor para a segurança reconectar em modo alerta

    def exit_DISCONNECTED(self):
        t = Timer(120.0, self.rest)
        t.start()

    def already_connected(self):
        print(f"O alarme '{self.name}' ja esta conectado!")


    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="alarm")
        self.name = device_name
        self.machine = Machine(model=self, states=AlarmState, initial=AlarmState.DEACTIVATED, after_state_change="notificar")

        self.machine.add_transition('activate', AlarmState.DEACTIVATED, AlarmState.ACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('activate', [AlarmState.RINGING, AlarmState.ALERT, AlarmState.ACTIVATED, AlarmState.DISCONNECTED], '=', after='activate_fail')
        self.machine.add_transition('ring', [AlarmState.ACTIVATED, AlarmState.ALERT], AlarmState.RINGING, unless='is_DISCONNECTED')
        self.machine.add_transition('ring', AlarmState.RINGING, '=')
        self.machine.add_transition('ring', [AlarmState.DISCONNECTED, AlarmState.DEACTIVATED], '=', after='ring_fail')
        self.machine.add_transition('stop', AlarmState.RINGING, AlarmState.ALERT, unless='is_DISCONNECTED')
        self.machine.add_transition('stop', [AlarmState.ACTIVATED, AlarmState.ALERT, AlarmState.DEACTIVATED, AlarmState.DISCONNECTED], '=', after='stop_fail')
        self.machine.add_transition('rest', AlarmState.ALERT, AlarmState.ACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('rest', [AlarmState.DEACTIVATED, AlarmState.ACTIVATED, AlarmState.DISCONNECTED, AlarmState.RINGING], '=', after='rest_fail')
        self.machine.add_transition('deactivate', AlarmState.ACTIVATED, AlarmState.DEACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('deactivate', [AlarmState.RINGING, AlarmState.ALERT], AlarmState.RINGING, unless='is_DISCONNECTED')
        self.machine.add_transition('deactivate', [AlarmState.DEACTIVATED, AlarmState.DISCONNECTED], '=', after='deactivate_fail')
        self.machine.add_transition('disconnection', '*', AlarmState.DISCONNECTED)
        self.machine.add_transition('reconnect', AlarmState.DISCONNECTED, AlarmState.ALERT, after='exit_DISCONNECTED')
        self.machine.add_transition('reconnect', [AlarmState.ACTIVATED, AlarmState.DEACTIVATED, AlarmState.RINGING, AlarmState.ALERT], '=', after='already_connected')



if __name__ == "__main__":
    s = Alarm('Principal')
    # log = Log()
    # rel = Report()
    # s.add_observer(log)
    # s.add_observer(rel)
    s.activate()
    s.stop()
    s.activate()
    # s.reconnect()
    # s.disconnection()
    # s.disconnection()
    s.stop()
    s.reconnect()
    print(s)
    print(s.__repr__())