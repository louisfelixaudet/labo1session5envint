# calcule pour la position 
import math

class AlgoPos:
    def __init__(self):
        self.DISTANCEROUE = 13

    def calculeOrientation(self, dd, dg): return (dd - dg) / self.DISTANCEROUE

    def calculeDistance(self, dd, dg): return (dd + dg) / 2

    def deplcementX(self, distance, anglePrecedant, angleActuel): return distance * math.cos(anglePrecedant + angleActuel / 2)

    def deplcementY(self, distance, anglePrecedant, angleActuel): return distance * math.sin(anglePrecedant + angleActuel / 2)

    def getX(self, xPrecedant, dx): return xPrecedant + dx

    def getY(self, yPrecedant, dy): return yPrecedant + dy

    def getOrientation(self, oriPrecedant, orientation): return oriPrecedant + orientation
