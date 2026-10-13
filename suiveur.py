import cv2
from detecteur_hsv import Detecteur_hsv
from ev_app_client_api import *
from robot import Robot
import param

def track_bar_cb(x):
    pass

def determinerPosition(image, centre):
    dy, dx = image.shape[:2]
    GAUCHE = 0
    MILIEU = 1
    DROITE = 2
    x, y = centre
    longueurSect = dx / 3
    if x >= 0 and x <= longueurSect:
        return GAUCHE
    elif x > longueurSect and x <= longueurSect * 2:
        return MILIEU
    elif x > longueurSect * 2 and x <= longueurSect * 3:
        return DROITE

titre_fenetre = "HSV Tester"

cv2.namedWindow(titre_fenetre)
cv2.createTrackbar('Hue min', titre_fenetre, 0, 179, track_bar_cb)
cv2.createTrackbar('Hue max', titre_fenetre, 0, 179, track_bar_cb)
cv2.createTrackbar('Sat min', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Sat max', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Val min', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Val max', titre_fenetre, 0, 255, track_bar_cb)

HUE_MIN = cv2.getTrackbarPos('Hue min', titre_fenetre)
HUE_MAX = cv2.getTrackbarPos('Hue max', titre_fenetre)
SAT_MIN = cv2.getTrackbarPos('Sat min', titre_fenetre)
SAT_MAX = cv2.getTrackbarPos('Sat max', titre_fenetre)
VAL_MIN = cv2.getTrackbarPos('Val min', titre_fenetre)
VAL_MAX = cv2.getTrackbarPos('Val max', titre_fenetre)

TEINTE_MIN = (HUE_MIN, SAT_MIN, VAL_MIN)
TEINTE_MAX = (HUE_MAX, SAT_MAX, VAL_MAX)
COULEUR_RECT = (0, 255, 0) # vert
GROSSEUR_TRAIT = 2
INTERVALLE = 30 # ms

SIZE_MIN_MOVE = 0
SIZE_MAX_STOP = 0
FORCE_TOURNER = 0.5
FORCE_AVANCER = 0.5

detecteur = Detecteur_hsv()
detecteur.demarrer()
image, image_disc, aire_max, p_hg, p_bd, centre = \
 detecteur.detecter(TEINTE_MIN, TEINTE_MAX)
cv2.imshow("image", image)

robot = Robot()
try:
    terminer = False
    while not terminer:

        HUE_MIN = cv2.getTrackbarPos('Hue min', titre_fenetre)
        HUE_MAX = cv2.getTrackbarPos('Hue max', titre_fenetre)
        SAT_MIN = cv2.getTrackbarPos('Sat min', titre_fenetre)
        SAT_MAX = cv2.getTrackbarPos('Sat max', titre_fenetre)
        VAL_MIN = cv2.getTrackbarPos('Val min', titre_fenetre)
        VAL_MAX = cv2.getTrackbarPos('Val max', titre_fenetre)

        TEINTE_MIN = (HUE_MIN, SAT_MIN, VAL_MIN)
        TEINTE_MAX = (HUE_MAX, SAT_MAX, VAL_MAX)

        image, image_disc, aire_max, p_hg, p_bd, centre = \
        detecteur.detecter(TEINTE_MIN, TEINTE_MAX)

        if aire_max > 0:
            cv2.rectangle(image, p_hg, p_bd, COULEUR_RECT, GROSSEUR_TRAIT)
            posobj = determinerPosition(image, centre)

        cv2.imshow("Image BGR", image)
        cv2.imshow("Image disc", image_disc)

        # <<-- Logiquement tu as juste a faire cette algo et tester -->>
        
        # Demande aussi au prof si la maniere dont on fait le programme principal est correct.

        # ICI la logique pour la poursuite de la balle
        if(aire_max >= SIZE_MIN_MOVE and aire_max <= SIZE_MAX_STOP):
            if (posobj == 0):
                gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORTLINE, param.GAUCHE, FORCE_TOURNER)
            elif (posobj == 1):
                gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORTLINE, param.AVANCER, FORCE_AVANCER)
            elif (posobj == 2):
                gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORTLINE, param.DROITE, FORCE_TOURNER)
        else:
            robot.arreter()

        choix = cv2.waitKey(INTERVALLE)
        if choix == ord('x'):
            terminer = True

except KeyboardInterrupt:
    print(f"CTRL-C")
finally:
    cv2.destroyAllWindows()
    detecteur.arreter()

    