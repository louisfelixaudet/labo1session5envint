from lireImage import Camera
import cv2

class Detecteur_hsv:
    def __init__(self):
        self.cam = Camera()

    def demarrer(self):
        self.cam.demarrer()

    def arreter(self):
        self.cam.arreter()

    def detecter(self, couleur_min, couleur_max):
        image = self.cam.capture()

        image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        image_binaire = cv2.inRange(image_hsv, couleur_min, couleur_max)

        contours, _ = cv2.findContours(image_binaire, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        aireMax = 0

        for c in contours:
            x, y, l, h = cv2.boundingRect(c)
            aire_rect = l * h
            if aireMax < aire_rect:
                dataRect = c

        if len(contours) == 0:
            dataRect = 0

        return image, image_binaire, self.aireMax(dataRect), self.p_haut_gauche(dataRect), self.p_bas_droite(dataRect), self.rect_centre(dataRect)

    def aireMax(self, c):
        if c == 0:
            return 0
        
        x, y, l, h = cv2.boundingRect(c)
        return l * h

    def p_haut_gauche(self, c):
        if c == 0:
            return 0

        x, y, l, h = cv2.boundingRect(c)
        return (x, y)

    def p_bas_droite(self, c):
        if c == 0:
            return 0

        x, y, l, h = cv2.boundingRect(c)
        return (x + l, y + h)

    def rect_centre(self, c):
        if c == 0:
            return 0

        x, y, l, h = cv2.boundingRect(c)
        return (x + l/2, y + h/2)


        
if __name__ == "__main__":
    terminer = False
    détecteur = Detecteur_hsv()
    détecteur.demarrer()

    while not terminer:
        cv2.imshow("image", cam.capture())
        choix = cv2.waitKey(30)
        if choix == ord('x'):
            terminer = True