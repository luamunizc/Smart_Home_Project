from devices.alarm import Alarm
from devices.cam import Cam
from devices.cat_feeder import CatFeeder
from devices.door import Door
from devices.lamp import Lamp
from devices.switch import Switch
from errors import *


class SmartHomeHub:
    def __init__(self):
        self.devices = dict()
        self.rotinas = dict()
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event: str, dados: dict):
        print(f"[EVENTO] {event}: {dados}")
        for observer in self._observers:
            observer.update(event, dados)

    def add_device(self, device_type, device_name=''):
        """
        Função para adicionar novos dispositivos ao SmartHomeHub a partir do tipo e nome
        Caso o nome seja uma string vazia, um nome padrao, na forma 'new_{type}' será criado
        Caso o nome dado já exista, será adicionado msm assim, porém renomeado adequadamente
        """

        # Tratando os nomes dos dispositivos, caso necessário
        if device_type not in self.devices.keys():
            self.devices[device_type] = dict()

        if device_name == '':
            device_name = f"new_{device_type}"

        if device_name in self.devices[device_type].keys():

            number = 1
            new_name = f"{device_name}_{number}"
            while new_name in self.devices[device_type].keys():
                number += 1
                new_name = f"{device_name}_{number}"
            device_name = new_name

        # adicionando os dispositivos nos dicionários dos seus respectivos tipos
        if device_type == 'alarm':
            new_device = Alarm(device_name)
            self.devices[device_type][new_device.name] = new_device

        elif device_type == 'cam':
            new_device = Cam(device_name)
            self.devices[device_type][new_device.name] = new_device

        elif device_type == 'cat_feeder':
            new_device = CatFeeder(device_name)
            self.devices[device_type][new_device.name] = new_device

        elif device_type == 'door':
            new_device = Door(device_name)
            self.devices[device_type][new_device.name] = new_device

        elif device_type == 'lamp':
            new_device = Lamp(device_name)
            self.devices[device_type][new_device.name] = new_device

        elif device_type == 'switch':
            new_device = Switch(device_name)
            self.devices[device_type][new_device.name] = new_device

        else:
            raise DeviceTypeInvalid(f"O dispositivo do tipo {device_type} nao existe na atual configuracao")


    def remove_device(self, device_type, device_name):
        self.devices[device_type].pop(device_name)
        if len(self.devices[device_type]) == 0:
            self.devices.pop(device_type)

    def print_list_all_devices(self):
        for i in self.devices:
            print(f"Dispositivo do tipo: {i}")
            for j in self.devices[i]:
                print(f"    {j}")

    def print_list_by_device_type(self, device_type):
        print(f"Dispositivo do tipo: {device_type}")
        for i in self.devices[device_type]:
            print(f"    {i}")

    def remove_all_by_type(self, device_type):
        self.devices.pop(device_type)

    def get_specific_device(self, device_type, device_name):
        return self.devices[device_type][device_name]



# testando

if __name__ == '__main__':
    casa = SmartHomeHub()
    casa.add_device('door', 'porta1')
    # print(casa.devices)
    # casa.remove_device('door', 'porta1')
    # print(casa.devices)
    casa.add_device('cam', 'camera1')
    casa.add_device('cam', 'camera1')
    casa.add_device('cat_feeder', 'alimentador')
    casa.add_device('cat_feeder', 'alimentador')
    casa.add_device('cat_feeder', 'alimentador')
    casa.add_device('cat_feeder', 'alimentador')
    casa.add_device('lamp')
    casa.add_device('switch')
    casa.add_device('switch')
    casa.add_device('switch')
    casa.add_device('switch')

    print(casa.get_specific_device('door', 'porta1'))
    casa.remove_all_by_type('cam')

    casa.print_list_all_devices()

    # for i in casa.devices.values():
    #     for j in i:
    #         print(i[j].name)
