from ev_app_client_api import *
from ev_app import *
import math
from algoPos import AlgoPos
import param


class ligne(EvApp):
    def __init__(self, port_no=param.NUM_PORT):
        super().__init__(port_no, tmo=0.02)
        self.MSG_INIT = 9
        self.algo = AlgoPos()
        self.startOrFinish()
        print("hello")

    def startOrFinish(self):
        gen_ev_externe("172.31.6.170", param.NUM_PORTLINE, self.MSG_INIT)

    def verifMetre(self, distance):
        return distance >= 100

    def dispatch_event(self, ev):
        if ev.type == 0:
            print("erreur")
            return

        if ev.type == 10:
            parts = ev.split()
            try:
                x, y, o = (float(p) for p in parts[:3])
                print(self.algo.calculeDistanceParcouru(x, y))
            except (ValueError, IndexError):
                print("ERROR: valeur non valide")
                return

            if self.verifMetre(self.algo.calculeDistanceParcouru(x, y)):
                self.startOrFinish()
        else:
            print("ERROR: message non connu")


if __name__ == "__main__":
    playLine = ligne()
    playLine.run()