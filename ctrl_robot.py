import time
from ev_app import *
from ev_app_client_api import *
from robot import Robot
from IMU import IMU
import param


class CtrlRobot(EvApp):
    def __init__(self, port_no):
        super().__init__(port_no, tmo=0.02)  # 20 ms pour un tick fiable
        self.robot = Robot()
        self.imu = IMU()
        self.en_mouvement = False
        self.startLIne = False
        self.x = 0
        self.y = 0
        self.orientation = 0
        self.dernierEnvoi = time.monotonic()
        self.calibrerMagnetometre()
        self.dernierImu = time.monotonic()
        self.dernierTick = self.dernierImu

    def _passif(self, duree):
        fin = time.monotonic() + duree
        dernier = time.monotonic()
        while time.monotonic() < fin:
            maintenant = time.monotonic()
            self.imu.obtenir_déplacement(False, maintenant - dernier)
            self.imu.obtenir_cap_magnétique()
            dernier = maintenant
            time.sleep(param.INTERVALLE_IMU)

    def calibrerMagnetometre(self):
        # Immobile: biais sur 20 échantillons. Puis 2 tours pour min/max de my, mz.
        print("Calibration: immobile")
        self._passif(1.0)
        print("Calibration: 2 tours")
        self.robot.tournerDroite(0.5)
        self.robot._maj_signes()
        angle = 0.0
        dernier = time.monotonic()
        while abs(angle) < 720.0:
            maintenant = time.monotonic()
            dt = maintenant - dernier
            dernier = maintenant
            angle, _ = self.imu.obtenir_déplacement(True, dt)
            self.imu.obtenir_cap_magnétique()
            time.sleep(param.INTERVALLE_IMU)
        self.robot.arreter()
        self.robot._maj_signes()
        self._passif(0.2)
        print("Calibration terminee")

    def envoyerImuSiTemps(self):
        maintenant = time.monotonic()
        if (maintenant - self.dernierImu) < param.INTERVALLE_IMU:
            return
        dt = maintenant - self.dernierTick
        self.dernierTick = maintenant
        self.dernierImu = maintenant
        angle, dist = self.imu.obtenir_déplacement(self.en_mouvement, dt)
        cap = self.imu.obtenir_cap_magnétique()
        if cap is None:
            cap = 0.0
        try:
            gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORT_PATROUILLE,
                           param.MSG_IMU_INFO, angle, dist, cap)
        except OSError:
            pass

    def envoyerPositionSiTemps(self):
        maintenant = time.monotonic()
        if self.startLIne and (maintenant - self.dernierEnvoi) >= param.INTERVALLE_ENVOI:
            o = self.robot.odom
            self.x, self.y, self.orientation = o.x, o.y, o.angle
            gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORTLINE,
                           param.MSG_POSITION, self.x, self.y, self.orientation)
            self.dernierEnvoi = maintenant

    def dispatch_event(self, ev):
        self.envoyerPositionSiTemps()
        self.envoyerImuSiTemps()

        if ev.type == 0:
            return

        donnee = ev.split()
        try:
            v = float(donnee[0]) if donnee and donnee[0] != "" else 0.0
        except ValueError:
            v = 0.0

        if ev.type == param.DROITE:
            self.en_mouvement = True
            self.robot.tournerDroite(v)
            self.robot._maj_signes()
        elif ev.type == param.AVANCER:
            self.en_mouvement = True
            self.robot.avancer(v)
            self.robot._maj_signes()
        elif ev.type == param.GAUCHE:
            self.en_mouvement = True
            self.robot.tournerGauche(v)
            self.robot._maj_signes()
        elif ev.type == param.RECULER:
            self.en_mouvement = True
            self.robot.reculer(v)
            self.robot._maj_signes()
        elif ev.type == param.AUG_SPEED:
            print(f"augmente de {v}")
        elif ev.type == param.DIM_SPEED:
            print(f"diminue de {v}")
        elif ev.type == param.ARRET:
            self.en_mouvement = False
            self.robot.arreter()
            self.robot._maj_signes()
        elif ev.type == param.STOP:
            self.en_mouvement = False
            self.robot.arreter()
            self.quitter_app()
            self.robot._maj_signes()
        elif ev.type == param.MSG_INIT:
            print("start line")
            self.startLIne = not self.startLIne
            if not self.startLIne:
                self.en_mouvement = False
                self.robot.arreter()
                self.robot._maj_signes()
                self.robot.odom.angle = 0
                self.robot.odom.x = 0
                self.robot.odom.y = 0
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