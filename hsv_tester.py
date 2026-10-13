# https://docs.opencv.org/4.5.1/da/d97/tutorial_threshold_inRange.html
import time
import cv2
import numpy as np
from lireImage import Camera
from detecteur_hsv import Detecteur_hsv

détecteur = Detecteur_hsv()
détecteur.demarrer()

hue_min, hue_max = 0, 179
sat_min, sat_max = 0, 255
val_min, val_max = 0, 255

print("Ctrl-C pour quitter.")

try:
    while True:
        image, image_disc, aire_max, p_hg, p_bd, centre = \
           détecteur.detecter((hue_min, sat_min, val_min), (hue_max, sat_max, val_max))

        if aire_max > 0:
            cv2.rectangle(image, p_hg, p_bd, (0, 255, 0))

        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    détecteur.arreter()