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
        self._observers = []

    def add_device(self, device_type, device_name=''):

        if device_type not in self.devices.keys():
            self.devices[device_type] = dict()

        if device_name == '':
            number = 1
            device_name = f"new_{device_type}_{number}"
            while device_name in self.devices[device_type].keys():
                number += 1
                device_name = f"new_{device_type}_{number}"

        # todo: consertar esses nomes

        number = 1
        while device_name in self.devices[device_type].keys():
            number += 1
            device_name = f"{device_name}_{number}"

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

    def get_especific_device(self, device_type, device_name):
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

    print(casa.get_especific_device('door', 'porta1'))
    casa.remove_all_by_type('cam')

    casa.print_list_all_devices()

    # for i in casa.devices.values():
    #     for j in i:
    #         print(i[j].name)
