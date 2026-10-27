# calcule pour la position 
import math
import numpy as np


DISTANCEROUE = 13
DIVTWO = 2
ANGLE = 180

def calculeOrientation(dd, dg): return (dd - dg) / DISTANCEROUE

def calculeDistance(dd, dg): return (dd + dg) / DIVTWO

def deplcementX(distance, anglePrecedant, angleActuel): return distance * math.cos(anglePrecedant + angleActuel / DIVTWO)

def deplcementY(distance, anglePrecedant, angleActuel): return distance * math.sin(anglePrecedant + angleActuel / DIVTWO)

def getX(xPrecedant, dx): return xPrecedant + dx

def getY(yPrecedant, dy): return yPrecedant + dy

def getOrientation(oriPrecedant, orientation): return oriPrecedant + orientation

def radianToDegree(angleRadian): return angleRadian * ANGLE/math.pi

def degreeToRadian(angleDegree): return angleDegree * math.pi/ANGLE

def calculeDistanceParcouru(x1, y1): return math.hypot(x1, y1)


# navigation inertiel fonction

def integralAx2Vx(dt, x, g):
    valuesVx = []
    Vx = 0
    axPrecedant = 0
    for ax in x:
        Vx += dt * (ax + axPrecedant) / DIVTWO * g
        axPrecedant = ax
        valuesVx.append(Vx)
    return valuesVx

def integralVx2Y(dt, x):
    valuesY = []
    y = 0
    vxPrecedant = 0
    for vx in x:
        y += dt * (vx + vxPrecedant) / DIVTWO
        vxPrecedant = vx
        valuesY.append(y)
    return valuesY

def valeurCorrection(max, min): return (max + min) / DIVTWO

def appCorrection(m, corr): return m - corr

def angleMinusPi2Pi(mz_corr, my_corr): 
    angle = np.arctan2(mz_corr, my_corr)
    if angle < 0 :
        angle += 2 * math.pi
    return radianToDegree(angle)





    