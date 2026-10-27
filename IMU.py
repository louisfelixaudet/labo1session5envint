from algoPos import *
import time
import param
import numpy as np
import math
from sonar import Lisseur 
from icm20948 import ICM20948

class IMU():
    def __init__(self):
        self.imu = ICM20948()
        self.maxMy = -math.inf
        self.minMy = math.inf
        self.maxMz = -math.inf
        self.minMz = math.inf
        self.lisseur_ay = Lisseur(param.FENETRE_DEP)
        self.lisseur_gx = Lisseur(param.FENETRE_DEP)
        self.vy = 0
        self.angle_rot = 0
        self.dist_y = 0
        self.g = 9.81
        self.ay_prec = 0
        self.gx_prec = 0
        self.vy_prec = 0
        self.biais_ay = 0
        self.biais_gx = 0


    def obtenir_cap_magnétique(self):
        try:
            mx, my, mz = self.imu.read_magnetometer_data()
            print(f"my:{my:.4f}, mz:{mz:.4f}")
        except:
            print("read value not possible")
            return 

        self.maxMy = max(self.maxMy, my)
        self.minMy = min(self.minMy, my)

        self.maxMz = max(self.maxMz, mz)
        self.minMz = min(self.minMz, mz)

        corr_my = valeurCorrection(self.maxMy, self.minMy)
        corr_mz = valeurCorrection(self.maxMz, self.minMz)

        my_corrige = appCorrection(my, corr_my)
        mz_corrige = appCorrection(mz, corr_mz)

        return angleMinusPi2Pi(mz_corrige, my_corrige) # check si la valeur de retour est la bonne lors du teste

    '''
        est_actif: est-ce que le robot est en mouvement
        dt: temps depuis la derniere appel de la methode
    '''
    def obtenir_déplacement(self, est_actif, dt):
        try:
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            print(f"ay:{ay:.4f}, gx:{gx:.4f}")
        except:
            print("read value not possible")
            return (self.angle_rot, self.dist_y)

        if not est_actif:
            self.vy = 0.0
            self.angle_rot = 0.0
            self.dist_y = 0.0
            self.ay_prec = 0.0
            self.vy_prec = 0.0
            self.gx_prec = 0.0
            self.biais_ay = self.lisseur_ay.lisser_min_max(ay)
            self.biais_gx = self.lisseur_gx.lisser_min_max(gx)
            
        else:
            ay -= self.biais_ay
            gx -= self.biais_gx
            self.vy += integralAx2Vx(dt, ay, self.ay_prec, self.g)
            self.dist_y += integralVx2Y(dt, self.vy, self.vy_prec)
            self.angle_rot += angleRotation(dt, gx, self.gx_prec)
            self.ay_prec = ay
            self.vy_prec = self.vy
            self.gx_prec = gx


        return (self.angle_rot, self.dist_y)

        

