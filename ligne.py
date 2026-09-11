# par default on commence toujours a la position (0, 0)
from ev_app_client_api import *
from ev_app import *
import math
from algoPos import AlgoPos 
import param

class ligne(EvApp):
    def __init__(self, port_no = param.NUM_PORT):
        super().__init__(port_no)
        self.MSG_INIT = "MSG_INIT"
        self.startOrFinish()
        self.algo = AlgoPos()

    def startOrFinish(self): gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, self.MSG_INIT)

    def verifMetre(self, disance): return disance > 100

    def dispatch_event(self, ev):

        if ev.type == "MSG_POSITION":

            estTabFloat = all(isinstance(x, float) for x in ev)

            if estTabFloat:
                x, y, o = ev
            else:
                print("ERROR: valeur non valide")
                return

            if self.verifMetre(self.algo.calculeDistanceParcouru(x, y)):
                self.startOrFinish()
        else:
            print("ERROR: message non connu")

if __name__ == "__main__":
    playLine = ligne()
    playLine.run()