import time
from ev_app import *
from ev_app_client_api import *
from robot import Robot
import param


class CtrlRobot(EvApp):
    def __init__(self, port_no):
        super().__init__(port_no, tmo=0.02)  # 20 ms pour un tick fiable
        self.robot = Robot()
        self.startLIne = False
        self.MSG_POSITION = 10
        self.MSG_RESTART = 11 
        self.x = 0
        self.y = 0
        self.orientation = 0

        self.INTERVALLE_ENVOI = 0.040  # 40 ms
        self.dernierEnvoi = time.monotonic()

    def envoyerPositionSiTemps(self):
        maintenant = time.monotonic()
        if self.startLIne and (maintenant - self.dernierEnvoi) >= self.INTERVALLE_ENVOI:
            o = self.robot.odom
            self.x, self.y, self.orientation = o.x, o.y, o.angle
            print(f"port: {param.NUM_PORTLINE}, message: {self.MSG_POSITION}, x: {self.x}, y: {self.y}, angle: {self.orientation}")
            gen_ev_externe("127.0.0.1", param.NUM_PORTLINE,
                           self.MSG_POSITION, self.x, self.y, self.orientation)
            self.dernierEnvoi = maintenant

    def dispatch_event(self, ev):
        self.envoyerPositionSiTemps()

        if ev.type == 0:
            return

        donnee = ev.split()
        try:
            v = float(donnee[0]) if donnee and donnee[0] != "" else 0.0
        except ValueError:
            v = 0.0

        if ev.type == 1:
            self.robot.tournerGauche(v)
            self.robot._maj_signes()
            gen_ev_externe("127.0.0.1", param.NUM_PORTLINE,
                                       self.MSG_RESTART)
        elif ev.type == 2:
            self.robot.avancer(v)
            self.robot._maj_signes()
        elif ev.type == 3:
            self.robot.tournerDroite(v)
            self.robot._maj_signes()
        elif ev.type == 4:
            self.robot.reculer(v)
            self.robot._maj_signes()
        elif ev.type == 5:
            print(f"augmente de {v}")
        elif ev.type == 6:
            print(f"diminue de {v}")
        elif ev.type == 7:
            self.robot.arreter()
            self.robot._maj_signes()
        elif ev.type == 8:
            self.robot.arreter()
            self.quitter_app()
            self.robot._maj_signes()
        elif ev.type == 9:
            print("start line")
            self.startLIne = not self.startLIne
            if not self.startLIne:
                self.robot.arreter()
                self.robot._maj_signes()
                print("Arrêt demandé par ligne.py", self.robot.odom)
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