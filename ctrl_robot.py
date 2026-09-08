from ev_app import *
from robot import Robot


class CtrlRobot(EvApp):
    def __init__(self, port_no):
        super().__init__(port_no)
        self.robot = Robot()

    def dispatch_event(self, ev):
        # timeout périodique d'EvApp — ignorer
        if ev.type == 0:
            return

        donnee = ev.split()
        try:
            v = float(donnee[0]) if donnee and donnee[0] != "" else 0.0
        except ValueError:
            v = 0.0

        if ev.type == 1:
            print(f"tourner gauche {v}")
            self.robot.tournerGauche(v)
        elif ev.type == 2:
            print(f"avancer robot {v}")
            self.robot.avancer(v)
        elif ev.type == 3:
            print(f"tourner droite {v}")
            self.robot.tournerDroite(v)
        elif ev.type == 4:
            print(f"reculer robot {v}")
            self.robot.reculer(v)
        elif ev.type == 5:
            print(f"augmente de {v}")
        elif ev.type == 6:
            print(f"diminue de {v}")
        elif ev.type == 7:
            print("ARRET")
            self.robot.arreter()
        elif ev.type == 8:
            print("QUITTER")
            self.robot.arreter()
            self.quitter_app()
        else:
            print("message invalide", ev)

    def quitter(self):
        try:
            self.robot.arreter()
        except Exception:
            pass
        print("Bye bye")


ctrl_robot = CtrlRobot(port_no=8000)
ctrl_robot.run()