import param
import threading
from ev_app_client_api import *
from gpiozero import DigitalOuputDevice

class Signaleur():
    def __init__(self):
        self.ligth = DigitalOuputDevice(4)
        self.timeLigth = None
        self._stop = threading.Event()
        self.thread = None

    def demarrer(self):
        self.thread.start()

    def arreter(self):
        self._stop.set()
        self.thread.join()

    def clignoter(self, time_light):
        if time_light < param.INTERVALLE_LIGHT:
            return

        self.timeLigth = time_light
        self.arreter()
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self.threadLumiere, )
        self.demarrer()

    def threadLumiere(self):
        while not self._stop.is_set():
            self.ligth.on()
            self._stop.wait(timeout=self.timeLigth / 2)
            self.ligth.off()
            self._stop.wait(timeout=self.timeLigth / 2)
        
        

class Lisseur():
    def __init__(self):
        pass

class Sonar():
    def __init__(self):
        self.trig = DigitalOuputDevice(12)
        self.echo = DigitalOuputDevice(13)
        self.valeurs_passees = []
        self.signaleur = Signaleur()
        self.signaleur.clignoter(5)

    def moyenMobile(self, nouvelle_valeur):
        FENETRE = 10

        self.valeurs_passees.append(nouvelle_valeur)
        if len(self.valeurs_passees)>FENETRE:
            del self.valeurs_passees[0]

        return sum(self.valeurs_passees)/len(self.valeurs_passees)

    def envoyerDistance(self, newDistance):
        gen_ev_externe(param.IP_ADRESSLINE, param.NUM_PORTLINE, param.MSG_SONAR, self.moyenMobile(newDistance))



