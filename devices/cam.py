from enum import Enum, auto
from transitions import Machine
from devices import Device


class CamState(Enum):
    DEACTIVATED = auto()
    IDLE = auto()
    STREAMING = auto()
    RECORDING = auto()
    REC_AND_STREAM = auto()
    DISCONNECTED = auto()

class Cam(Device):

    def on_enter_DEACTIVATED(self):
        print(f'Câmera {self.name} desativada')

    def on_enter_IDLE(self):
        print(f'Câmera {self.name} em modo espera')

    def on_enter_STREAMING(self):
        print(f"Câmera {self.name} está em modo de apenas transmissão")

    def on_enter_RECORDING(self):
        print(f"Câmera {self.name} está em modo de apenas gravação")

    def on_enter_REC_AND_STREAM(self):
        print(f"Câmera {self.name} está em modo de transmissão e gravação")

    def on_enter_DISCONNECTED(self):
        print(f"Câmera {self.name} desconectada")

    def is_DISCONNECTED(self):
        return self.state == CamState.DISCONNECTED

    def saved_state(self):
        self.before_disconnection = self.state

    def restore_state(self):
        target_state = self.before_disconnection
        print(f"Câmera {self.name} reconectada")
        if target_state == CamState.RECORDING:
            self.start_recording()
        elif target_state == CamState.STREAMING:
            self.start_streaming()
        elif target_state == CamState.REC_AND_STREAM:
            self.start_recording()
            self.start_streaming()

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="cam")
        self.name = device_name
        self.machine = Machine(model=self, states=CamState, initial=CamState.DEACTIVATED)

        self.machine.add_transition('deactivate', '*', CamState.DEACTIVATED, unless='is_DISCONNECTED')
        self.machine.add_transition('turn_on', CamState.DEACTIVATED, CamState.IDLE, unless='is_DISCONNECTED')
        self.machine.add_transition('start_recording', CamState.IDLE, CamState.RECORDING, unless='is_DISCONNECTED')
        self.machine.add_transition('start_recording', CamState.STREAMING, CamState.REC_AND_STREAM, unless='is_DISCONNECTED')
        self.machine.add_transition('start_streaming', CamState.IDLE, CamState.STREAMING, unless='is_DISCONNECTED')
        self.machine.add_transition('start_streaming', CamState.RECORDING, CamState.REC_AND_STREAM, unless='is_DISCONNECTED')
        self.machine.add_transition('stop_recording', CamState.RECORDING, CamState.IDLE, unless='is_DISCONNECTED')
        self.machine.add_transition('stop_recording', CamState.REC_AND_STREAM, CamState.STREAMING, unless='is_DISCONNECTED')
        self.machine.add_transition('stop_streaming', CamState.STREAMING, CamState.IDLE, unless='is_DISCONNECTED')
        self.machine.add_transition('stop_streaming', CamState.REC_AND_STREAM, CamState.RECORDING, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnected', '*', CamState.DISCONNECTED, before='saved_state')
        self.machine.add_transition('reconnect', CamState.DISCONNECTED, CamState.IDLE, after='restore_state')

