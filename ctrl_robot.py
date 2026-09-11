from ev_app import *
from ev_app_client_api import *
from robot import Robot
import param


class CtrlRobot(EvApp):
    def __init__(self, port_no):
        super().__init__(port_no)
        self.robot = Robot()
        self.startLIne = False
        self.MSG_POSITION = "MSG_POSITION"
        self.x = 0
        self.y = 0
        self.orientation = 0
        self.xPrecendant = 0
        self.yPrecendant = 0
        self.orientationPrecendant = 0

    def dispatch_event(self, ev):
        # algo Ligne
        if ev.type == "MSG_INIT":
            self.startLIne = not self.startLIne

        if self.startLIne:
            gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORT, self.MSG_POSITION, self.x, self.y, self.orientaion)
        
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
            self.robot._maj_signes()
            print(self.robot.odom)
        elif ev.type == 2:
            print(f"avancer robot {v}")
            self.robot.avancer(v)
            self.robot._maj_signes()
            print(self.robot.odom)
        elif ev.type == 3:
            print(f"tourner droite {v}")
            self.robot.tournerDroite(v)
            self.robot._maj_signes()
            print(self.robot.odom)
        elif ev.type == 4:
            print(f"reculer robot {v}")
            self.robot.reculer(v)
            self.robot._maj_signes()
            print(self.robot.odom)
        elif ev.type == 5:
            print(f"augmente de {v}")
        elif ev.type == 6:
            print(f"diminue de {v}")
        elif ev.type == 7:
            print("ARRET")
            self.robot.arreter()
            self.robot._maj_signes()
            print(self.robot.odom)
        elif ev.type == 8:
            print("QUITTER")
            self.robot.arreter()
            self.quitter_app()
            self.robot._maj_signes()
            print(self.robot.odom)
        else:
            print("message invalide", ev)

    def quitter(self):
        try:
            self.robot.arreter()
        except Exception:
            pass
        print("Bye bye")


ctrl_robot = CtrlRobot(port_no=param.NUM_PORT)
ctrl_robot.run()