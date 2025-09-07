from enum import Enum, auto
from transitions import Machine
from devices import Device, console


class LampState(Enum):
    ON = auto()
    OFF = auto()
    DISCONNECTED = auto()

class Colour(Enum):
    QUENTE = auto()
    FRIA = auto()
    NEUTRA = auto()

class Lamp(Device):

    def is_DISCONNECTED(self):
        return self.state == LampState.DISCONNECTED

    def save_state(self):
        self.before_disconnection = {
            "state": self.state,
            "colour": self.colour,
            "brightness": self.brightness
        }

    def restore_state(self):
        self.colour = self.before_disconnection["colour"]
        self.brightness = self.before_disconnection["brightness"]
        print(f"Lampada {self.name} reconectada")
        if self.before_disconnection["state"] == LampState.ON:
            self.on()

    def change_colour(self, new_colour: Colour):
        if self.is_DISCONNECTED():
            print("Ação falhou: a lâmpada está desconectada.")
            return
        if isinstance(new_colour, Colour):
            self.colour = new_colour
            if new_colour == Colour.QUENTE:
                cor = "navajo_white1"
            elif new_colour == Colour.FRIA:
                cor = "pale_turquoise1"
            elif new_colour == Colour.NEUTRA:
                cor = "grey93"
            console.print(f"Cor da lâmpada '{self.name}' alterada para {new_colour.name}", style=cor)
        else:
            print("Erro: Cor inválida.")

    def change_brightness(self, level: int):
        if self.is_DISCONNECTED():
            print("Ação falhou: a lâmpada está desconectada.")
            return
        if 1 <= level <= 100:
            self.brightness = level
            print(f"Brilho da lâmpada '{self.name}' ajustado para {level}%.")
        else:
            print("Erro: Brilho inválido, selecione valor entre 0 e 100.")

    def __init__(self, device_name: str):
        super().__init__(device_name=device_name, device_type="lamp")
        self._colour = Colour.NEUTRA
        self._brightness = 100
        self.before_disconnection = {
            "state": LampState.OFF,
            "colour": self.colour,
            "brightness": self.brightness
        }
        self.machine = Machine(model=self, states=LampState, initial=LampState.OFF)
        self.machine.add_transition('on', LampState.OFF, LampState.ON, unless='is_DISCONNECTED')
        self.machine.add_transition('off', LampState.ON, LampState.OFF, unless='is_DISCONNECTED')
        self.machine.add_transition('disconnect', '*', LampState.DISCONNECTED, before='save_state')
        self.machine.add_transition('reconnect', LampState.DISCONNECTED, LampState.OFF, after='restore_state')


if __name__ == "__main__":
    l = Lamp("lamp")
    l.on()
    l.change_colour(Colour.QUENTE)
    l.change_colour(Colour.FRIA)
    l.change_colour(Colour.NEUTRA)