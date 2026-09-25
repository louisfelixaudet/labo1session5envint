import threading
import time

import param
from ev_app_client_api import *
from gpiozero import DigitalInputDevice, DigitalOutputDevice


class Signaleur:

    def __init__(self, gpio):
        self.led = DigitalOutputDevice(gpio)
        self.periode = None
        self._stop = threading.Event()
        self.thread = None

    def demarrer(self):
        if self.thread is not None and not self.thread.is_alive():
            self.thread.start()

    def arreter(self):
        self._stop.set()
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()
        self.thread = None
        self.led.off()

    def clignoter(self, periode):
        if periode < param.INTERVALLE_LIGHT:
            return

        self.arreter()
        self.periode = periode
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._boucle, daemon=True)
        self.demarrer()

    def _boucle(self):
        while not self._stop.is_set():
            self.led.on()
            self._stop.wait(self.periode / 2)
            if self._stop.is_set():
                break
            self.led.off()
            self._stop.wait(self.periode / 2)
        self.led.off()

    def close(self):
        self.arreter()
        self.led.close()


class Lisseur:
    def __init__(self, grandeur):
        self.grandeur = grandeur
        self._fenetre = []
        self._fenetre_mm = []

    def _pousser(self, fenetre, valeur):
        fenetre.append(valeur)
        if len(fenetre) > self.grandeur:
            del fenetre[0]

    def lisser(self, valeur):
        self._pousser(self._fenetre, valeur)
        return sum(self._fenetre) / len(self._fenetre)

    def lisser_min_max(self, valeur):
        self._pousser(self._fenetre_mm, valeur)
        valeurs = self._fenetre_mm
        # Il faut au moins 3 échantillons pour retirer le min et le max
        # et garder de quoi moyenner.
        if len(valeurs) < 3:
            return sum(valeurs) / len(valeurs)
        gardees = list(valeurs)
        gardees.remove(min(gardees))
        gardees.remove(max(gardees))
        return sum(gardees) / len(gardees)


class Sonar:
    def __init__(self, trig, echo, led):
        self.trig = DigitalOutputDevice(trig)
        self.trig.off()
        self.echo = DigitalInputDevice(echo, pull_up=False)
        self.echo.when_activated = self._front_montant
        self.echo.when_deactivated = self._front_descendant
        self.lisseur = Lisseur(param.FENETRE_SONAR)
        self.signaleur = Signaleur(led)
        self._t0 = None
        self._periode = None
        self.signaleur.clignoter(param.PERIODE_DEL_CALME)
        self._periode = param.PERIODE_DEL_CALME

    def mesurer(self):
        self._t0 = None
        self.trig.off()
        time.sleep(0.000002)
        self.trig.on()
        time.sleep(0.000010)
        self.trig.off()

    def arreter(self):
        self.signaleur.arreter()

    def close(self):
        self.signaleur.close()
        self.trig.close()
        self.echo.close()

    def _front_montant(self):
        self._t0 = time.perf_counter()

    def _front_descendant(self):
        t0 = self._t0
        self._t0 = None
        if t0 is None:
            return
        duree = time.perf_counter() - t0
        if duree <= 0:
            return

        distance = param.VITESSE_SON * duree / 2.0 
        if distance < param.DIST_MIN_SONAR:
            return
        if distance > param.DIST_MAX_SONAR:
            distance = param.DIST_MAX_SONAR
        self._publier(distance)

    def _periode_del(self, distance):
        if distance < param.SEUIL_PROCHE_CM:
            return param.PERIODE_DEL_PROCHE
        if distance < param.SEUIL_ALERTE_CM:
            return param.PERIODE_DEL_ALERTE
        return param.PERIODE_DEL_CALME

    def _publier(self, brut):
        distance = self.lisseur.lisser_min_max(brut)
        periode = self._periode_del(distance)
        if periode != self._periode:
            self._periode = periode
            self.signaleur.clignoter(periode)
        if distance < param.SEUIL_ALERTE_CM:
            gen_ev_externe(
                param.IP_ADRESSLINE, param.NUM_PORTLINE,
                param.MSG_SONAR, distance,
            )
        print(f"sonar: {distance:.1f} cm")


def main():
    gauche = Sonar(param.TRIG_SONAR_G, param.ECHO_SONAR_G, param.DEL_JAUNE)
    droite = Sonar(param.TRIG_SONAR_D, param.ECHO_SONAR_D, param.DEL_VERTE)

    demi = param.PERIODE_MESURE / 2
    try:
        while True:
            gauche.mesurer()
            time.sleep(demi)
            droite.mesurer()
            time.sleep(demi)
    except KeyboardInterrupt:
        print("arrêt des sonars")
    finally:
        gauche.close()
        droite.close()


if __name__ == "__main__":
    main()
