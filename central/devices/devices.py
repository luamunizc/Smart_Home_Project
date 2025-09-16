from rich.console import Console
from datetime import datetime
import csv

console = Console()

class Device:
    def __init__(self, device_type: str, device_name: str):
        self.name = device_name
        self.type = device_type
        self._observers = []

    def to_dict(self):
        return {'name': self.name, 'type': self.type, 'state': self.state.value}

    def __str__(self):
        return f"Dispositivo {self.name} do tipo {self.type} no estado {self.state.name}"

    def notificar(self):
        new_log = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ' , ' + self.__str__() + '\n'
        with open(r'data/log.csv', 'a', newline='') as csvfile:
            csvfile.write(new_log)
            for observer in self._observers:
                observer.update()

    def add_observer(self, observer_func):
        self._observers.append(observer_func)

    def meu_observador(self):
        print(f"Observer: {self.name} esta agora no estado {self.state.name}")
        with open('data/log.csv', 'a') as logging:
            logging.write(f"{datetime.today()} - {self.name} mudou para {self.state.name}\n")