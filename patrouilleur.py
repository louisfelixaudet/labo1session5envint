import time
from ev_app import *
from ev_app_client_api import *
import param

FORCE_AVANCER = 0.6
FORCE_TOURNER = 1
DISTANCE_M = 1.0
TOURNER = 180.0
REPOS = 0.2


class Patrouilleur(EvApp):
    def __init__(self):
        super().__init__(param.NUM_PORT_PATROUILLE, tmo=0.2)
        self.phase = "avancer"
        self.phase_suivante = "avancer"
        self.debut = True
        self.fin_repos = 0.0

    def envoyer(self, msg, force):
        gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, msg, force)

    def _stop_puis(self, suivante):
        self.envoyer(param.ARRET, 0)
        self.phase = "repos"
        self.phase_suivante = suivante
        self.fin_repos = time.monotonic() + REPOS

    def dispatch_event(self, ev):
        if ev.type != param.MSG_IMU_INFO:
            return
        try:
            angle, dist, _cap = (float(p) for p in ev.split()[:3])
        except (ValueError, IndexError):
            return

        if self.debut:
            self.debut = False
            self.envoyer(param.AVANCER, FORCE_AVANCER)
            return

        if self.phase == "repos":
            if time.monotonic() < self.fin_repos:
                return
            self.phase = self.phase_suivante
            if self.phase == "tourner":
                self.envoyer(param.DROITE, FORCE_TOURNER)
            else:
                self.envoyer(param.AVANCER, FORCE_AVANCER)
            return

        if self.phase == "avancer" and abs(dist) >= DISTANCE_M:
            print(f"1 m ({dist:.2f}), pivot")
            self._stop_puis("tourner")
        elif self.phase == "tourner" and abs(angle) >= TOURNER:
            print(f"180 deg ({angle:.0f}), avance")
            self._stop_puis("avancer")

    def quitter(self):
        try:
            self.envoyer(param.ARRET, 0)
        except Exception:
            pass


patrouilleur = Patrouilleur()
patrouilleur.run()
