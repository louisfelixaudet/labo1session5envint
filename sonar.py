import param
import threading
from gpiozero import DigitalOuputDevice

class Signaleur():
    def __init__(self, timeLight):
        self.ligth = DigitalOuputDevice(4)
        self.timeLigth = timeLight
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
        pass

