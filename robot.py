from gpiozero import DigitalOutputDevice, PWMOutputDevice

class Robot:
    def __init__(self):
        self.Droite = 0
        self.Gauche = 0
        # Setup GPIO pins
        self.in1 = DigitalOutputDevice(6)   # In1
        self.in2 = DigitalOutputDevice(5)   # In2
        self.ena = PWMOutputDevice(13, frequency=1000)  # EnA
        self.in3 = DigitalOutputDevice(15)  # In3
        self.in4 = DigitalOutputDevice(14)  # In4
        self.enb = PWMOutputDevice(18, frequency=1000)  # EnB
        # Setup PWM
        self.pwm_ena = self.ena
        self.pwm_enb = self.enb
        self.pwm_ena.value = 0
        self.pwm_enb.value = 0

    def avancer(self, puissance):
        self.in1.on()   # In1
        self.in2.off()  # In2
        self.in3.on()   # In3
        self.in4.off()  # In4
        self.pwm_ena.value = puissance
        self.pwm_enb.value = puissance

    def reculer(self, puissance):
        self.in1.off()  # In1
        self.in2.on()   # In2
        self.in3.off()  # In3
        self.in4.on()   # In4
        self.pwm_ena.value = puissance
        self.pwm_enb.value = puissance

    # Difference(diff): 0: ne tourne pas (ligne droite), 0.5: le cote inferieur ne tourne pas ses roues, 1: le cote inferieur a ses roues a contre-sens (tourne sur place)
    def tournerDroite(self, puissance, diff=1):
        vg = puissance
        vd = puissance * (1 - 2 * diff)
        self.in1.on()   
        self.in2.off()
        self.pwm_ena.value = vg
        if vd >= 0:
            self.in3.on()
            self.in4.off()
            self.pwm_enb.value = vd
        else:
            self.in3.off()
            self.in4.on()
            self.pwm_enb.value = -vd

    def tournerGauche(self, puissance, diff=1):
        vg = puissance * (1 - 2 * diff)
        vd = puissance 
        self.in3.on()   
        self.in4.off()
        self.pwm_enb.value = vd
        if vg >= 0:
            self.in1.on()
            self.in2.off()
            self.pwm_ena.value = vg
        else:
            self.in1.off()
            self.in2.on()
            self.pwm_ena.value = -vg

    def arreter(self):
        self.pwm_ena.value = 0
        self.pwm_enb.value = 0
        self.in1.off()  # In1
        self.in2.off()  # In2
        self.in3.off()  # In3
        self.in4.off()  # In4

    def __del__(self):
        self.arreter()
        self.in1.close()
        self.in2.close()
        self.in3.close()
        self.in4.close()
        self.ena.close()
        self.enb.close()

class Moteur:
    def __init__(self, pin):
        self.pin = pin
        self.pwm = PWMOutputDevice(pin, frequency=1000)
        self.pwm.value = 0

    def setP(self, puissance):
        self.pwm.value = puissance / 100.0

    def arreter(self):
        self.pwm.value = 0
        self.pwm.close()