from algoPos import *
import time
import numpy as np
from icm20948 import ICM20948

class IMU():
    def __init__(self):
        self.imu = ICM20948()
        self.dt = 0.05
        self.xs = np.arange(0, 5, self.dt)
        self.maxMy = 0
        self.minMy = 0
        self.maxMz = 0
        self.minMz = 0

    def obtenir_cap_magnétique(self):
        try:
            mx, my, mz = self.imu.read_magnetometer_data()
            print(f"my:{my:.4f}, mz:{mz:.4f}")
        except:
            print("read value not possible")

        self.maxMy = max(self.maxMy, my)
        self.minMy = min(self.minMy, my)

        self.maxMz = max(self.maxMz, mz)
        self.minMz = min(self.minMz, mz)

        corr_my = valeurCorrection(self.maxMy, self.minMy)
        corr_mz = valeurCorrection(self.maxMz, self.minMz)

        my_corrige = appCorrection(my, corr_my)
        mz_corrige = appCorrection(mz, corr_mz)

        return angleMinusPi2Pi(mz_corrige, my_corrige)

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

        if not est_actif:
            pass
        elif est_actif:
            pass
        else:
            print("Data non valide")

        

