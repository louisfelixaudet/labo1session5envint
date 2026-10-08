# https://docs.opencv.org/4.5.1/da/d97/tutorial_threshold_inRange.html
import cv2
import numpy as np
from lireImage import Camera
from detecteur_hsv import Detecteur_hsv

def track_bar_cb(x):
    pass

détecteur = Detecteur_hsv()
détecteur.demarrer()

titre_fenetre = "HSV Tester"
cv2.namedWindow(titre_fenetre)
cv2.createTrackbar('Hue min', titre_fenetre, 0, 179, track_bar_cb)
cv2.createTrackbar('Hue max', titre_fenetre, 0, 179, track_bar_cb)
cv2.createTrackbar('Sat min', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Sat max', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Val min', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Val max', titre_fenetre, 0, 255, track_bar_cb)

print(f"Pour quitter presser la touche 'q'.")
print(f"Pour rafraichir presser la touche.")

terminer = False
while not terminer:

    hue_min = cv2.getTrackbarPos('Hue min', titre_fenetre)
    hue_max = cv2.getTrackbarPos('Hue max', titre_fenetre)
    sat_min = cv2.getTrackbarPos('Sat min', titre_fenetre)
    sat_max = cv2.getTrackbarPos('Sat max', titre_fenetre)
    val_min = cv2.getTrackbarPos('Val min', titre_fenetre)
    val_max = cv2.getTrackbarPos('Val max', titre_fenetre)

    image, image_disc, aire_max, p_hg, p_bd, centre = \
       détecteur.detecter((hue_min, sat_min, val_min), (hue_max, sat_max, val_max))

    if aire_max > 0:
        cv2.rectangle(image, p_hg, p_bd, (0, 255, 0))

    cv2.imshow("Image BGR", image)
    cv2.imshow("Image disc", image_disc)

    choix = cv2.waitKey(200)
    if  choix == ord('q'):
        terminer = True    

cv2.destroyAllWindows()
détecteur.arreter()