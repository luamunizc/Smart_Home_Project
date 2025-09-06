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
    def __init__(self, device_name: str):
        super().__init__(device_type="cam")
        self.name = device_name
        self.machine = Machine(model=self, states=CamState, initial=CamState.DEACTIVATED)

        self.machine.add_transition('deactivate', CamState.IDLE, CamState.DEACTIVATED)
        self.machine.add_transition('turn_on', CamState.DEACTIVATED, CamState.IDLE)
        self.machine.add_transition('record',
                                    [CamState.IDLE, CamState.STREAMING, CamState.REC_AND_STREAM],
                                    CamState.RECORDING)
        self.machine.add_transition('stream', [CamState.IDLE, CamState.RECORDING, CamState.REC_AND_STREAM],
                                    CamState.STREAMING)
        self.machine.add_transition('stream_rec', [CamState.IDLE, CamState.RECORDING, CamState.STREAMING],
                                    CamState.REC_AND_STREAM)
        self.machine.add_transition('disconnected', '*', CamState.DISCONNECTED)
        self.machine.add_transition('reconnect', CamState.DISCONNECTED, CamState.IDLE)

