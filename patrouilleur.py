from ev_app_client_api import *
from ev_app import *
from IMU import IMU
import math
import param

imu = IMU()

DISTANCE = 100
TOURNER = 180
FORCE_AVANCER = 0.5
FORCE_TOURNER = 0.5

try:
    terminer = False
    while not terminer:
        while(imu.obtenir_déplacement < DISTANCE):
            gen_ev_externe(gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, param.AVANCER, FORCE_AVANCER))
        while(imu.obtenir_cap_magnétique < TOURNER):
            gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, param.DROITE, FORCE_TOURNER)

except KeyboardInterrupt:
    print(f"CTRL-C")
finally:
    gen_ev_externe(param.IP_ADRESS, param.NUM_PORT, param.ARRET, 0)


    
    