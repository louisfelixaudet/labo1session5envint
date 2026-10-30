import time
from ev_app_client_api import *
from IMU import IMU
import param

imu = IMU()

DISTANCE = 100       # cm. dist_y revient en mètres
TOURNER = 180        # degrés
FORCE_AVANCER = 0.5
FORCE_TOURNER = 0.5
INTERVALLE = 0.04

def envoyer(msg, force):
    gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, msg, force)

def repos(duree):
    envoyer(param.ARRET, 0)
    fin = time.monotonic() + duree
    dernier = time.monotonic()
    while time.monotonic() < fin:
        maintenant = time.monotonic()
        dt = maintenant - dernier
        dernier = maintenant
        imu.obtenir_déplacement(False, dt)
        time.sleep(INTERVALLE)

try:
    repos(1.0)
    while True:
        dernier = time.monotonic()
        dist_cm = 0.0
        while dist_cm < DISTANCE:
            maintenant = time.monotonic()
            dt = maintenant - dernier
            dernier = maintenant
            _, dist_m = imu.obtenir_déplacement(True, dt)
            dist_cm = dist_m * 100
            envoyer(param.AVANCER, FORCE_AVANCER)
            time.sleep(INTERVALLE)

        repos(0.3)

        dernier = time.monotonic()
        angle = 0.0
        while abs(angle) < TOURNER:
            maintenant = time.monotonic()
            dt = maintenant - dernier
            dernier = maintenant
            angle, _ = imu.obtenir_déplacement(True, dt)
            envoyer(param.DROITE, FORCE_TOURNER)
            time.sleep(INTERVALLE)

        repos(0.3)
except KeyboardInterrupt:
    print("CTRL-C")
finally:
    envoyer(param.ARRET, 0)
