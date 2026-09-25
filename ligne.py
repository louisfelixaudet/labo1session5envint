from ev_app_client_api import *
from ev_app import *
import math
from algoPos import AlgoPos
import param


class ligne(EvApp):
    def __init__(self, port_no=param.NUM_PORTLINE):
        super().__init__(port_no, tmo=0.02)
        self.algo = AlgoPos()
        self.distance_parcourue = 0.0
        self.dist_sonar = {}
        self.arrete_par_sonar = False
        self.startOrFinish()
        print("hello")

    def startOrFinish(self):
        gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, param.MSG_INIT)

    def verifMetre(self, distance):
        return distance >= 100

    def _commander_robot(self, msg, puissance=0):
        gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, msg, puissance)

    def _sur_sonar(self, ev):
        parts = ev.split()
        try:
            distance = float(parts[0])
        except (ValueError, IndexError):
            print("ERROR: distance sonar non valide")
            return
        if len(parts) > 1:
            try:
                self.dist_sonar[int(float(parts[1]))] = distance
                distance = min(self.dist_sonar.values())
            except ValueError:
                pass
        print(f"sonar {distance:.1f} cm")

        if distance < param.SEUIL_ARRET_CM:
            self.arrete_par_sonar = True
            self._commander_robot(param.ARRET, 0)
            return

        # Entre 20 et 30 cm on ne change rien : ça évite d'osciller.
        if distance > param.SEUIL_REPRISE_CM and self.arrete_par_sonar:
            if self.verifMetre(self.distance_parcourue):
                return
            self.arrete_par_sonar = False
            self._commander_robot(param.AVANCER, param.PUISSANCE_REPRISE)

    def dispatch_event(self, ev):
        if ev.type == 0:
            #print(f"erreur: {ev}")
            return

        if ev.type == param.MSG_POSITION:
            print("type 10 recu")
            parts = ev.split()
            try:
                x, y, o = (float(p) for p in parts[:3])
                self.distance_parcourue = self.algo.calculeDistanceParcouru(x, y)
                print(self.distance_parcourue)
            except (ValueError, IndexError):
                print("ERROR: valeur non valide")
                return

            if self.verifMetre(self.distance_parcourue):
                self.arrete_par_sonar = False
                self.startOrFinish()
                self.startOrFinish()
        elif ev.type == param.MSG_SONAR:
            self._sur_sonar(ev)
        else:
            print("ERROR: message non connu")


if __name__ == "__main__":
    playLine = ligne()
    playLine.run()