from rich.console import Console
from enum import Enum
from transitions import Machine
from devices import Device

console = Console()

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

    def __init__(self, device_name: str):
        super().__init__(device_type='switch')
        self.name = device_name
        self.before_disconnection = SwitchState.OFF
        self.machine = Machine(model=self, states=SwitchState, initial=SwitchState.OFF)
        self.machine.add_transition('on', SwitchState.OFF, SwitchState.ON, unless='is_DISCONNECTED')
        self.machine.add_transition('off', SwitchState.ON, SwitchState.OFF, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnected', '*', SwitchState.DISCONNECTED, before='saved_state')
        self.machine.add_transition('reconnect', SwitchState.DISCONNECTED, SwitchState.OFF, after='restore_state' )
