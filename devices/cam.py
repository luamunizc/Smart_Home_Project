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
    def __init__(self):
        super().__init__()
        self.machine = Machine(model=self, states=CamState, initial=CamState.DEACTIVATED)

        self.machine.add_transition('desativar', CamState.IDLE, CamState.DEACTIVATED)
        self.machine.add_transition('ligar', CamState.DEACTIVATED, CamState.IDLE)
        self.machine.add_transition('gravar',
                                    [CamState.IDLE, CamState.STREAMING, CamState.REC_AND_STREAM],
                                    CamState.RECORDING)
        self.machine.add_transition('transmitir', [CamState.IDLE, CamState.RECORDING, CamState.REC_AND_STREAM],
                                    CamState.STREAMING)
        self.machine.add_transition('streamgravado', [CamState.IDLE, CamState.RECORDING, CamState.STREAMING],
                                    CamState.REC_AND_STREAM)
        self.machine.add_transition('desconexao', '*', CamState.DISCONNECTED)
        self.machine.add_transition('reconectar', CamState.DISCONNECTED, CamState.IDLE)

