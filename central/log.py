class Observer:
    def __init__(self, name):
        self.nome = name

    def mostrar_msg(self):
        print(f"Recebendo msg")
        print(f"{self.nome}")


class Log:
    def __init__(self):
        self.observers = []
        self.evento = Observer("Evento")
        self.log = Observer("Primeiro log de lua")


    def notificar_log(self):
        self.log.mostrar_msg()
    def notificar_varios(self):
        for i in range(len(self.observers)):
            self.observers[i].mostrar_msg()
obs = Observer("Observador do comp de lua")
l = Log()
for j in range(20):
    l.observers.append(Observer(f"{j} observador"))
l.notificar_varios()


l.notificar_log()