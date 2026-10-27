from algoPos import *
import time
import numpy as np
from icm20948 import ICM20948

class IMU():
    def __init__(self):
        self.imu = ICM20948()
        self.dt = 0.05
        self.xs = np.arange(0, 5, self.dt)

    def obtenir_cap_magnétique(self, ):
        pass

    def obtenir_déplacement(self, ):
        pass

    