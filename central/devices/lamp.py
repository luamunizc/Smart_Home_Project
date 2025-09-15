from enum import Enum, auto
from transitions import Machine
from devices.devices import Device, console



class LampState(Enum):
    LIGADO = auto()
    DESLIGADO = auto()
    DESCONECTADO = auto()

class Colour(Enum):
    QUENTE = auto()
    FRIA = auto()
    NEUTRA = auto()

class Lamp(Device):

    def is_DESCONECTADO(self):
        return self.state == LampState.DESCONECTADO

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
        if self.before_disconnection["state"] == LampState.LIGADO:
            self.on()

    def change_colour(self, new_colour: str):
        if self.is_DESCONECTADO():
            print("Ação falhou: a lâmpada está desconectada.")
            return
        if new_colour == "QUENTE":
            new_colour = Colour(1)
        elif new_colour == "FRIA":
            new_colour = Colour(2)
        elif new_colour == "NEUTRA":
            new_colour = Colour(3)

        if isinstance(new_colour, Colour):
            self._colour = new_colour
            if new_colour == Colour.QUENTE:
                cor = "navajo_white1"
            elif new_colour == Colour.FRIA:
                cor = "pale_turquoise1"
            elif new_colour == Colour.NEUTRA:
                cor = "grey93"
            console.print(f"Cor da lâmpada '{self.name}' alterada para {Colour(new_colour).name}", style=cor)
        else:
            print("Erro: Cor inválida.")

    def pick_colour(self):
        console.print(f"A cor atual da lampada é {self._colour.name}", style=self._colour)

    def change_brightness(self, level: int):
        if self.is_DESCONECTADO():
            print("Ação falhou: a lâmpada está desconectada.")
            return
        if 1 <= level <= 100:
            self._brightness = level
            print(f"Brilho da lâmpada '{self.name}' ajustado para {level}%.")
        elif level == 0:
            self.off()
            print(f"Lampada {self.name} desligada")
        else:
            print("Erro: Brilho inválido, selecione valor entre 0 e 100.")

    def __init__(self, device_name: str, colour=Colour.NEUTRA, brightness=100):
        super().__init__(device_name=device_name, device_type="lamp")
        self._colour = colour
        self._brightness = brightness
        self.before_disconnection = {
            "state": LampState.DESLIGADO,
            "colour": self._colour,
            "brightness": self._brightness
        }
        self.machine = Machine(model=self, states=LampState, initial=LampState.DESLIGADO)
        self.machine.add_transition('on', LampState.DESLIGADO, LampState.LIGADO, unless='is_DESCONECTADO')
        self.machine.add_transition('on', LampState.LIGADO, '=')
        self.machine.add_transition('off', LampState.LIGADO, LampState.DESLIGADO, unless='is_DESCONECTADO')
        self.machine.add_transition('off', LampState.DESLIGADO, '=')
        self.machine.add_transition('disconnect', [LampState.LIGADO, LampState.DESLIGADO], LampState.DESCONECTADO, before='save_state')
        self.machine.add_transition('disconnect', LampState.DESCONECTADO, '=')
        self.machine.add_transition('reconnect', LampState.DESCONECTADO, LampState.DESLIGADO, after='restore_state')
        self.machine.add_transition('reconnect', [LampState.LIGADO, LampState.DESLIGADO], '=')

    def to_dict(self):
        return {'name': self.name, 'type': self.type, 'colour': self._colour.name, 'brilho': self._brightness, 'state': self.state.value}

    def __str__(self):
        return f"Dispositivo {self.name} do tipo {self.type} de cor {self._colour.name} e brilho {self._brightness}% no estado {self.state.name}"

if __name__ == "__main__":

    l = Lamp("lamp")
    print(l)
    l.on()
    print(l)
    l.change_colour(Colour.QUENTE)
    l.change_colour(Colour.FRIA)
    l.change_colour(Colour.NEUTRA)