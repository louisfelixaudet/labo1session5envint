from ev_app_client_api import *
import time
import keyboard
import param

class telecom():
    def __init__(self, port=param.NUM_PORT):
        self.port = port
        self.run = True
        # m/s = power
        self.power = 0
        self.directAct = 0

        self.dictMove = {
            'q': [param.DROITE, 0.7],
            'w': [param.AVANCER, 0.4],
            'e': [param.GAUCHE, 0.7],
            's': [param.RECULER, 0.6],
            '.': [param.AUG_SPEED, 0.05],
            ',': [param.DIM_SPEED, -0.05],
            'space': [param.ARRET, 0],
            'x': [param.STOP, 0]
        }

    def ReadKey(self):
        strike = 0
        while self.run:
            key = keyboard.read_key()
            strike = self.dictMove.get(key, [0, 0])
            self.directAct = self.ChooseMove(strike[0])
            self.PowerServing(strike)
            print(self.power)
            print(strike)
            return strike[0]

    def StopHandler(self, code):
        if code == 0: print ("tapper une touche valide")
        if code == param.ARRET: self.power = 0
        if code == param.STOP:
            print ("Program has been stop")
            self.run = False
            self.power = 0


    def PowerServing(self, strike):
        if  strike[0] == param.DROITE or strike[0] == param.GAUCHE:
            self.power = strike[1]
        elif strike[0] == param.AVANCER or strike[0] == param.RECULER and self.power == 0:
            self.power = strike[1]
        elif self.directAct == param.AVANCER or self.directAct == param.RECULER and strike[0] == param.AUG_SPEED or strike[0] == param.DIM_SPEED:
            self.power = max(0.0, min(1.0, self.power + strike[1]))
        else:
            self.power = 0.0

    def ChooseMove(self, move):
        if move in (param.AUG_SPEED, param.DIM_SPEED, param.ARRET, param.STOP):
            return self.directAct
        else:
            return move

    def message_a_envoyer(self, code):
        if code in (param.AUG_SPEED, param.DIM_SPEED):
            if self.directAct in (param.DROITE, param.AVANCER, param.GAUCHE, param.RECULER):
                return self.directAct
            return None
        return code


    def SendMSG(self, move):
        gen_ev_externe(param.IP_ADRESS, self.port, move, self.power)

                

telecommande = telecom()
while telecommande.run:
    code = telecommande.ReadKey()
    telecommande.StopHandler(code)
    msg = telecommande.message_a_envoyer(code)
    if msg is not None:
        telecommande.SendMSG(msg)
    time.sleep(0.15)
    
    