from devices.alarm import Alarm, AlarmState
from devices.cam import Cam, CamState
from devices.door import Door, DoorState
from devices.feeder import Feeder, FeederState
from devices.lamp import Lamp, LampState
from devices.switch import Switch, SwitchState
from errors import *
from threading import Lock
import json
from observers import Log, Report


class SmartHomeHub:

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SmartHomeHub, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        if hasattr(self, '_initialized'):
            return

        self.devices = dict()
        self.rotinas = dict()
        self._observers = []
        self.observer_logs = Log()
        self.observer_relatorios = Report()
        self._initialized = True

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event: str, dados: dict):
        print(f"[EVENTO] {event}: {dados}")
        for observer in self._observers:
            observer.notificar()

    def add_device(self, device={}, device_name=''):
        """
        Função para adicionar novos dispositivos ao SmartHomeHub a partir do tipo e nome
        Caso o nome seja uma string vazia, um nome padrao, na forma 'new_{type}' será criado
        Caso o nome dado já exista, será adicionado msm assim, porém renomeado adequadamente
        """
        if "name" in device.keys():
            device_name = device["name"]

        if device_name == '':
            device_name = f"new_{device['type']}"

        if device_name in self.devices.keys():

            number = 1
            new_name = f"{device_name}_{number}"
            while new_name in self.devices.keys():
                number += 1
                new_name = f"{device_name}_{number}"
            device_name = new_name

        # adicionando os dispositivos nos dicionários dos seus respectivos tipos
        if device['type'] == 'alarm':
            new_device = Alarm(device_name)
            if 'state' in device.keys():
                new_device.state = AlarmState(device['state'])

        elif device['type'] == 'cam':
            new_device = Cam(device_name)
            if 'state' in device.keys():
                new_device.state = CamState(device['state'])

        elif device['type'] == 'porta':
            new_device = Door(device_name)
            if 'state' in device.keys():
                new_device.state = DoorState(device['state'])

        elif device['type'] == 'feeder':
            new_device = Feeder(device_name)
            if 'state' in device.keys():
                new_device.state = FeederState(device['state'])
            if 'level' in device.keys():
                new_device.level = device['level']

        elif device['type'] == 'lamp':
            new_device = Lamp(device_name)
            if 'state' in device.keys():
                new_device.state = LampState(device['state'])
            if 'colour' in device:
                new_device.change_colour(device['colour'])
            if 'brilho' in device:
                new_device._brightness = device['brilho']

        elif device['type'] == 'tomada':
            new_device = Switch(device_name)
            if 'state' in device.keys():
                new_device.state = SwitchState(device['state'])
            if 'potencia_w' in device:
                new_device._potencia_w = device['potencia_w']

        else:
            raise DeviceTypeInvalid(f"O dispositivo do tipo {device['type']} nao existe na atual configuracao")

        self.devices[new_device.name] = new_device


    def remove_device(self, device_name):
        print(f"Realmente quer excluir o dispositivo {device_name}?"
              f"s = sim     | qualquer outra selecao cancela a operacao")
        sel = input().lower().strip()
        if sel == 's':
            self.devices.pop(device_name)
        else:
            print(f"Operacao de exclusao do dispositivo {device_name} cancelada")


    def print_list_all_devices(self):
        for i in self.devices.values():
            print(i.__str__())


    def get_specific_device(self, device_name):
        if device_name in self.devices.keys():
            return self.devices.get(device_name)
        else:
            return f"Nenhum dispositivo com o nome {device_name} encontrado"

    def salvar_configuracao(self, caminho_arquivo: str):

        print(f"Salvando configuracao em '{caminho_arquivo}'...")

        config_data = {
            "dispositivos": {},
            "rotinas": self.rotinas
        }

        for device in self.devices.values():
            config_data["dispositivos"][device.name] = device.to_dict()

        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            print("Configuracao salva com sucesso.")
        except IOError as e:
            print(f"ERRO: Nao foi possivel salvar a configuracao em '{caminho_arquivo}': {e}")

    def comeca(self):
        try:
            with open("./data/casa.json", 'r') as file:
                tudo = json.load(file)
                for device in tudo['dispositivos'].values():
                    self.add_device(device)
        except FileNotFoundError:
            print(f"Arquivo de permanencia nao encontrado")
        except:
            print(f"Aconteceu um erro inesperado")


    def lista(self):

        lista = list(self.devices.values())
        for ind in range(len(lista)):
            print(f"{ind}. {lista[ind].name}")
        return lista


    def usando_alarm(self, nome, uso):

        while True:
            print(f"Opcoes do alarme {nome}:\n"
                  f"1. ativar\n"
                  f"2. desativar\n"
                  f"3. reconectar\n"
                  f"4. pausar\n"
                  f"5. parar\n")
            print('Ou digite s para sair')
            sel = input().lower().strip()
            if sel == '1':
                uso.activate()
            elif sel == '2':
                uso.deactivate()
            elif sel == '3':
                uso.reconnect()
            elif sel == '4':
                uso.rest()
            elif sel == '5':
                uso.stop()
            elif sel == 's':
                break

    def usando_cam(self, nome, uso):

        while True:
            print(f"Opcoes de camera {nome}:\n"
                  f"1. ativar\n"
                  f"2. desativar\n"
                  f"3. reconectar\n"
                  f"4. gravar\n"
                  f"5. transmitir\n"
                  f"6. parar gravacao\n"
                  f"7. parar transmissao\n"
                  f"8. desconectar\n")
            print('Ou digite s para sair')
            sel = input().lower().strip()
            if sel == '1':
                uso.activate()
            elif sel == '2':
                uso.deactivate()
            elif sel == '3':
                uso.reconnect()
            elif sel == '4':
                uso.start_recording()
            elif sel == '5':
                uso.start_streaming()
            elif sel == '6':
                uso.stop_recording()
            elif sel == '7':
                uso.stop_streaming()
            elif sel == '8':
                uso.disconnect()
            elif sel == 's':
                break

    def usando_porta(self, nome, uso):

        while True:
            print(f"Opcoes de porta {nome}:\n"
                  f"1. abrir\n"
                  f"2. fechar\n"
                  f"3. trancar\n"
                  f"4. destrancar\n"
                  f"5. reconectar\n"
                  f"6. desconectar\n")
            print('Ou digite s para sair')
            sel = input().lower().strip()
            if sel == '1':
                uso.open()
            elif sel == '2':
                uso.close()
            elif sel == '3':
                uso.lock()
            elif sel == '4':
                uso.unlock()
            elif sel == '5':
                uso.reconnect()
            elif sel == '6':
                uso.disconnect()
            elif sel == 's':
                break

    def usando_feeder(self, nome, uso):

        while True:
            print(f"Opcoes de alimentador {nome}:\n"
                  f"1. definir reservatorio como cheio\n"
                  f"2. encher pote\n"
                  f"3. desconectar\n"
                  f"4. reconectar\n")
            print('Ou digite s para sair')
            sel = input().lower().strip()
            if sel == '1':
                uso.refill()
            elif sel == '2':
                uso.feed()
            elif sel == '3':
                uso.disconnect()
            elif sel == '4':
                uso.reconnect()
            elif sel == 's':
                break

    def usando_lamp(self, nome, uso):

        while True:
            print(f"Opcoes de lampada {nome}:\n"
                  f"1. ligar\n"
                  f"2. desligar\n"
                  f"3. desconectar\n"
                  f"4. reconectar\n")
            print('Ou digite s para sair')
            sel = input().lower().strip()
            if sel == '1':
                uso.on()
            elif sel == '2':
                uso.off()
            elif sel == '3':
                uso.disconnect()
            elif sel == '4':
                uso.reconnect()
            elif sel == 's':
                break

    def usando_switch(self, nome, uso):

        while True:
            print(f"Opcoes de tomada {nome}:\n"
                  f"1. ligar\n"
                  f"2. desligar\n"
                  f"3. desconectar\n"
                  f"4. reconectar\n")
            print('Ou digite s para sair')
            sel = input().lower().strip()
            if sel == '1':
                uso.on()
            elif sel == '2':
                uso.off()
            elif sel == '3':
                uso.disconnect()
            elif sel == '4':
                uso.reconnect()
            elif sel == 's':
                break


    def usar(self, nome):
        if nome in self.devices.keys():
            usando = self.devices.get(nome)
            if usando.type == 'alarm':
                self.usando_alarm(nome, usando)
            elif usando.type == 'cam':
                self.usando_cam(nome, usando)
            elif usando.type == 'porta':
                self.usando_porta(nome, usando)
            elif usando.type == 'feeder':
                self.usando_feeder(nome, usando)
            elif usando.type == 'lamp':
                self.usando_lamp(nome, usando)
            elif usando.type == 'tomada':
                self.usando_switch(nome, usando)

    def atributos(self, nome):

        usando = self.devices.get(nome)
        if usando.type in ('alarm', 'cam', 'porta', 'feeder'):
            print(f"Dispositivos do tipo {usando.type} nao tem atributos a serem alterados")
        elif usando.type == 'lamp':
            while True:
                print(f"Trocar cor ou brilho? (C/b)\n"
                      f"Escolha s para sair")

                atrb = input().lower().strip()
                if atrb == 'c':

                    while True:
                        print(f"Escolha a cor da lampada entre as opcoes abaixo:\n"
                              f"1. Quente\n"
                              f"2. Fria\n"
                              f"3. Neutra\n"
                              f"Ou digite s para sair\n")
                        sel = input().lower().strip()
                        if sel == '1':
                            usando.change_colour('QUENTE')
                            break
                        elif sel == '2':
                            usando.change_colour('FRIA')
                            break
                        elif sel == '3':
                            usando.change_colour('NEUTRA')
                            break
                        elif sel == 's':
                            print(f"Operacao abortada")
                            break
                        else:
                            print(f"Comando invalido")

                elif atrb == 'b':

                    while True:
                        print(f"Digite o valor de brilho desejado")
                        brl = int(input())
                        if 0 < brl <= 100:
                            usando.change_brightness(brl)
                            break
                elif atrb == 's':
                    break

        elif usando.type == 'tomada':
            print(f"Escolha a potencia da tomada {usando.name}")
            while True:
                pot = int(input())
                if  pot < 0: # Confesso que nao entendo o suficiente de eletronica para saber qual deveria ser o limite superior disso
                    print(f"Entrada negativa invalida!")
                else:
                    break
            usando._potencia_w = pot

def nome_dispositivo():
    nome = input('Digite o nome do dispositivo:')
    return nome.lower().strip()

def selecao_dispositivo():
    while True:
        print("Dispositivos disponiveis:\n"
              "1. Alarme de seguranca\n"
              "2. Camera de seguranca\n"
              "3. Alimentador automatico para pets\n"
              "4. Porta\n"
              "5. Lampada\n"
              "6. Tomada")
        tipo = input("Escolha o tipo de dispositivo:")
        if tipo == '1':
            return 'alarm'
        elif tipo == '2':
            return 'cam'
        elif tipo == '3':
            return 'feeder'
        elif tipo == '4':
            return 'porta'
        elif tipo == '5':
            return 'lamp'
        elif tipo == '6':
            return 'tomada'
        else:
            print("Erro ao selecionar dispositivo")

def sel_disponiveis(lista):
    while True:
        try:
            selecao = int(input("Selecione o numero de dispositivo:"))
            if selecao < len(lista):
                return lista[selecao].name
        except:
            print("Erro ao selecionar dispositivo")



# testando

# if __name__ == '__main__':
#     casa = SmartHomeHub()
#     casa.add_device('porta', 'porta1')
#     print(casa.devices)
#     casa.remove_device('porta', 'porta1')
#     casa.add_device('cam', 'camera1')
#     casa.add_device('cam', 'camera1')
#     casa.add_device('feeder', 'alimentador')
#     casa.add_device('feeder', 'alimentador')
#     casa.add_device('feeder', 'alimentador')
#     casa.add_device('feeder', 'alimentador')
#     casa.add_device('lamp')
#     print(casa.devices['lamp'])
#     casa.add_device('tomada')
#     casa.add_device('tomada')
#     casa.add_device('tomada')
#     casa.add_device('tomada')
#     print(casa.devices)
#
#     print(casa.get_specific_device('porta', 'porta1'))
#     casa.remove_all_by_type('cam')
#
#     casa.print_list_all_devices()

    # for i in casa.devices.values():
    #     for j in i:
    #         print(i[j].name)
