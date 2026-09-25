IP_ADRESS="172.31.6.202"
NUM_PORT=8000
IP_ADRESSLINE="127.0.0.1"
NUM_PORTLINE=8001
MSG_INIT = 9
MSG_POSITION = 10
MSG_SONAR = 11
INTERVALLE_ENVOI = 0.040
DROITE = 3
GAUCHE = 1
AVANCER = 2
RECULER = 4
ARRET = 7
STOP = 8
AUG_SPEED = 5
DIM_SPEED = 6
INTERVALLE_LIGHT = 0.05

# Broches BCM, schéma « Le robot mobile »
TRIG_SONAR_G = 8
ECHO_SONAR_G = 25
DEL_JAUNE = 10          # indicateur du sonar gauche
TRIG_SONAR_D = 21
ECHO_SONAR_D = 20
DEL_VERTE = 9           # indicateur du sonar droit

VITESSE_SON = 343       # m/s
DIST_MIN_SONAR = 2      # cm, plancher du HC-SR04
DIST_MAX_SONAR = 400    # cm, plafond du HC-SR04
FENETRE_SONAR = 10
PERIODE_MESURE = 0.1    # 10 mesures par seconde

# Clignotement : < 30 cm, < 50 cm, sinon
SEUIL_PROCHE_CM = 30
SEUIL_ALERTE_CM = 50
PERIODE_DEL_PROCHE = 0.100
PERIODE_DEL_ALERTE = 0.500
PERIODE_DEL_CALME = 5.0

# ligne.py : arrêt sous 20 cm, reprise au-dessus de 30 cm
SEUIL_ARRET_CM = 20
SEUIL_REPRISE_CM = 30
PUISSANCE_REPRISE = 0.4   # même puissance que la touche « w »