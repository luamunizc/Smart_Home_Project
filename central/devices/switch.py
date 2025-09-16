from enum import Enum
from transitions import Machine
import time
from devices.devices import Device, console


# Me confundi e traduzi tomada para switch em vez de outlet, mas não vai fazer diferença no uso

class SwitchState(Enum):
    DESLIGADO = 0
    LIGADO = 1
    DESCONECTADO = 2

class Switch(Device):

    def on_enter_LIGADO(self):
        self.notificar(f"Tomada {self.name} ligada")

    def on_enter_DESLIGADO(self):
        self.notificar(f"Tomada {self.name} desligada")

    def on_enter_DESCONECTADO(self):
        self.notificar(f"Tomada {self.name} desconectada")

    def saved_state(self):
        self.before_disconnection = self.state

    def restore_state(self):
        target_state = self.before_disconnection
        self.notificar(f"Tomada {self.name} reconectada")
        if target_state == SwitchState.LIGADO:
            self.on()

    def is_DESCONECTADO(self):
        return self.state == SwitchState.DESCONECTADO

    @property
    def potencia_w(self):
        return self._potencia_w

    @potencia_w.setter
    def potencia_w(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Potência deve ser um inteiro não negativo.")
        self._potencia_w = value

    def _start_consumption_tracking(self):
        self._last_on_timestamp = time.time()

    def _calculate_consumption(self):
        if self._last_on_timestamp:
            delta_seconds = time.time() - self._last_on_timestamp
            delta_hours = delta_seconds / 3600
            self.consumo_wh += self.potencia_w * delta_hours
            print(
                f"Consumo nesta sessão: {self.potencia_w * delta_hours:.4f} Wh. Total acumulado: {self.consumo_wh:.4f} Wh.")
            self._last_on_timestamp = None

    def __init__(self, device_name: str, potencia_w: int = 20):
        super().__init__(device_name=device_name, device_type='tomada')
        self._potencia_w = 0
        self.potencia_w = potencia_w

        self.consumo_wh = 0.0
        self._last_on_timestamp = None
        self.before_disconnection = SwitchState.DESLIGADO
        self.machine = Machine(model=self, states=SwitchState, initial=SwitchState.DESLIGADO, after_state_change="notificar")
        self.machine.add_transition('on', SwitchState.DESLIGADO, SwitchState.LIGADO, unless='is_DESCONECTADO', after='_start_consumption_tracking')
        self.machine.add_transition('on', [SwitchState.LIGADO, SwitchState.DESCONECTADO], '=')
        self.machine.add_transition('off', SwitchState.LIGADO, SwitchState.DESLIGADO, unless='is_DESCONECTADO', before='_calculate_consumption')
        self.machine.add_transition('off', [SwitchState.DESCONECTADO, SwitchState.DESLIGADO], '=')
        self.machine.add_transition('disconnect', [SwitchState.LIGADO, SwitchState.DESLIGADO], SwitchState.DESCONECTADO, before='saved_state')
        self.machine.add_transition('disconnect', SwitchState.DESCONECTADO, '=')
        self.machine.add_transition('reconnect', SwitchState.DESCONECTADO, SwitchState.DESLIGADO, after='restore_state')
        self.machine.add_transition('reconnect', [SwitchState.LIGADO, SwitchState.DESLIGADO], '=')


    def to_dict(self):
        return {'name': self.name, 'type': self.type, 'potencia_w': self._potencia_w, 'state': self.state.value}

    def __str__(self):
        return f"Dispositivo {self.name} do tipo {self.type} de potencia {self._potencia_w} no estado {self.state.name}"