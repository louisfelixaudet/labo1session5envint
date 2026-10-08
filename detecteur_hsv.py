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
        dataRect = None

        for c in contours:
            x, y, l, h = cv2.boundingRect(c)
            aire_rect = l * h
            if aireMax < aire_rect:
                aireMax = aire_rect
                dataRect = c

        return image, image_binaire, self.aireMax(dataRect), self.p_haut_gauche(dataRect), self.p_bas_droite(dataRect), self.rect_centre(dataRect)

    def aireMax(self, c):
        if c is None:
            return 0
        
        x, y, l, h = cv2.boundingRect(c)
        return l * h

    def p_haut_gauche(self, c):
        if c is None:
            return 0

        x, y, l, h = cv2.boundingRect(c)
        return (x, y)

    def p_bas_droite(self, c):
        if c is None:
            return 0

        x, y, l, h = cv2.boundingRect(c)
        return (x + l, y + h)

    def rect_centre(self, c):
        if c is None:
            return 0

        x, y, l, h = cv2.boundingRect(c)
        return (x + l/2, y + h/2)


        
if __name__ == "__main__":
    def track_bar_cb(x):
        pass

    detecteur = Detecteur_hsv()
    detecteur.demarrer()

    titre_fenetre = "HSV Tester"
    cv2.namedWindow(titre_fenetre)
    cv2.createTrackbar('Hue min', titre_fenetre, 0, 179, track_bar_cb)
    cv2.createTrackbar('Hue max', titre_fenetre, 0, 179, track_bar_cb)
    cv2.createTrackbar('Sat min', titre_fenetre, 0, 255, track_bar_cb)
    cv2.createTrackbar('Sat max', titre_fenetre, 0, 255, track_bar_cb)
    cv2.createTrackbar('Val min', titre_fenetre, 0, 255, track_bar_cb)
    cv2.createTrackbar('Val max', titre_fenetre, 0, 255, track_bar_cb)

    print("Pour quitter presser la touche 'q'.")

    terminer = False
    while not terminer:
        hue_min = cv2.getTrackbarPos('Hue min', titre_fenetre)
        hue_max = cv2.getTrackbarPos('Hue max', titre_fenetre)
        sat_min = cv2.getTrackbarPos('Sat min', titre_fenetre)
        sat_max = cv2.getTrackbarPos('Sat max', titre_fenetre)
        val_min = cv2.getTrackbarPos('Val min', titre_fenetre)
        val_max = cv2.getTrackbarPos('Val max', titre_fenetre)

        image, image_disc, aire_max, p_hg, p_bd, centre = \
            detecteur.detecter((hue_min, sat_min, val_min), (hue_max, sat_max, val_max))

        cv2.imshow("Image BGR", image)
        cv2.imshow("Image disc", image_disc)

        choix = cv2.waitKey(200)
        if choix == ord('q'):
            terminer = True

    cv2.destroyAllWindows()
    detecteur.arreter()