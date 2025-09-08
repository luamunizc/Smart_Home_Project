from enum import Enum
from transitions import Machine
from central.devices.devices import Device, console
import time


# Me confundi e traduzi tomada para switch em vez de outlet, mas não vai fazer diferença no uso

class SwitchState(Enum):
    OFF = 0
    ON = 1
    DISCONNECTED = 2

class Switch(Device):

    def on_enter_ON(self):
        console.print(f"Tomada {self.name} ligada", style="bold green")

    def on_enter_OFF(self):
        console.print(f"Tomada {self.name} desligada", style="bold bright_red")

    def on_enter_DISCONNECTED(self):
        console.print(f"Tomada {self.name} desconectada", style="bold color(166)")

    def saved_state(self):
        self.before_disconnection = self.state

    def restore_state(self):
        target_state = self.before_disconnection
        console.print(f"Tomada {self.name} reconectada", style="bold color(122)")
        if target_state == SwitchState.ON:
            self.on()

    def is_DISCONNECTED(self):
        return self.state == SwitchState.DISCONNECTED

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

    def __init__(self, device_name: str, potencia_w: int = 0):
        super().__init__(device_name=device_name, device_type='switch')
        self._potencia_w = 0
        self.potencia_w = potencia_w

        self.consumo_wh = 0.0
        self._last_on_timestamp = None
        self.before_disconnection = SwitchState.OFF
        self.machine = Machine(model=self, states=SwitchState, initial=SwitchState.OFF)
        self.machine.add_transition('on', SwitchState.OFF, SwitchState.ON, unless='is_DISCONNECTED', after='_start_consumption_tracking')
        self.machine.add_transition('off', SwitchState.ON, SwitchState.OFF, unless='is_DISCONNECTED', before='_calculate_consumption')
        self.machine.add_transition('disconnected', '*', SwitchState.DISCONNECTED, before='saved_state')
        self.machine.add_transition('reconnect', SwitchState.DISCONNECTED, SwitchState.OFF, after='restore_state' )
