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

        if device_name in self.devices[device_type].keys():
            number = 1
            device_name = f"{device_name}_{number}"
            while device_name in self.devices[device_type].keys():
                number += 1
                device_name = f"{device_type}_{number}"

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
            raise DeviceTypeInvalid(f"Esse tipo de dispositivo nao existe na atual configuracao")


# testando

if __name__ == '__main__':
    casa = SmartHomeHub()
    casa.add_device('door', 'porta1')
    casa.add_device('cam', 'camera1')
    casa.add_device('cam', 'camera1')
    casa.add_device('cat_feeder', 'alimentador')
    casa.add_device('ddd')
    casa.add_device('lamp')
    casa.add_device('switch')


    for i in casa.devices.values():
        for j in i:
            print(i[j].name)
