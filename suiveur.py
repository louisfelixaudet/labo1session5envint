import cv2
from detecteur_hsv import Detecteur_hsv
from ev_app_client_api import *
from robot import Robot
import param

def track_bar_cb(x):
    pass

GAUCHE = 0
MILIEU = 1
DROITE = 2

def determinerPosition(image, centre):
    dy, dx = image.shape[:2]
    x, y = centre
    longueurSect = dx / 3
    if x >= 0 and x <= longueurSect:
        return GAUCHE
    elif x > longueurSect and x <= longueurSect * 2:
        return MILIEU
    elif x > longueurSect * 2 and x <= longueurSect * 3:
        return DROITE


HUE_MIN = 2
HUE_MAX = 57
SAT_MIN = 144
SAT_MAX = 246
VAL_MIN = 89
VAL_MAX = 255

TEINTE_MIN = (HUE_MIN, SAT_MIN, VAL_MIN)
TEINTE_MAX = (HUE_MAX, SAT_MAX, VAL_MAX)
COULEUR_RECT = (0, 255, 0) # vert
GROSSEUR_TRAIT = 2
INTERVALLE = 30 # ms

SIZE_MIN_MOVE = 300
SIZE_MAX_STOP = 15000
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

        HUE_MIN = 2
        HUE_MAX = 57
        SAT_MIN = 144
        SAT_MAX = 246
        VAL_MIN = 89
        VAL_MAX = 255

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
            if (posobj == GAUCHE):
                gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORTLINE, param.GAUCHE, FORCE_TOURNER)
            elif (posobj == MILIEU):
                gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORTLINE, param.AVANCER, FORCE_AVANCER)
            elif (posobj == DROITE):
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

    