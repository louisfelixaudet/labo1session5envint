import cv2
from detecteur_hsv import Detecteur_hsv
from ev_app_client_api import *

def determinerPosition(image, centre):
    dy, dx = image.shape
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


detecteur = Detecteur_hsv()
detecteur.demarrer()
image, image_disc, aire_max, p_hg, p_bd, x_c, y_c = \
 detecteur.detecter(TEINTE_MIN, TEINTE_MAX)
cv2.imshow("image", image)


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

        image, image_disc, aire_max, p_hg, p_bd, x_c, y_c = \
        detecteur.detecter(TEINTE_MIN, TEINTE_MAX)

        if aire_max > 0:
            cv2.rectangle(image, p_hg, p_bd, COULEUR_RECT, GROSSEUR_TRAIT)
            determinerPosition(image, (x_c, y_c))

        cv2.imshow("Image BGR", image)
        cv2.imshow("Image disc", image_disc)

        # <<-- Logiquement tu as juste a faire cette algo et tester -->>
        # utilise la fonction determinerPosition pour trouver la position de la balle
        # Demande aussi au prof si la maniere dont on fait le programme principal est correct.

        # ICI la logique pour la poursuite de la balle
        # Si la surface est plus petite qu’un minimum
        # (déterminé par expériences), le robot ne bouge pas car
        # c’est peu probable que cela soit la balle ou alors elle
        # est trop loin;
        # Si la surface est plus grande qu’un maximum
        # (déterminé par expériences), le robot ne bouge pas
        # car la balle est trop proche;
        # Si la balle est au centre et que sa surface est correcte,
        # le robot avance;
        # Si la balle est à gauche de l’image, le robot tourne à gauche;
        # Si la balle est à droite de l’image, le robot tourne à droite;

        choix = cv2.waitKey(INTERVALLE)
        if choix == ord('x'):
            terminer = True
except KeyboardInterrupt:
    print(f"CTRL-C")
finally:
    cv2.destroyAllWindows()
    detecteur.arreter()

    