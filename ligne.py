# par default on commence toujours a la position (0, 0)
from ev_app_client_api import *
from ev_app import *
import math
import param

class ligne(EvApp):
    def __init__(self, port_no = param.NUM_PORT):
        super().__init__(port_no)
        self.MSG_INIT = "MSG_INIT"

    def calculeDistanceParcouru(self, x1, y1): return math.abs(math.sqrt((x1 - 0)^2 + (y1 - 0)^2))

    def startOrFinish(self): gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, self.MSG_INIT)

    def verifMetre(self, disance): return disance > 100

    def dispatch_event(self, ev):
        donnee = ev.split()

        if ev.type == "MSG_POSITION":

            estTabFloat = all(isinstance(x, float) for x in ev)

            if estTabFloat:
                x, y, o = ev
            else:
                print("ERROR: valeur non valide")
                return

            if self.verifMetre(self.calculeDistanceParcouru(x, y)):
                self.startOrFinish()
        else:
            print("ERROR: message non connu")

