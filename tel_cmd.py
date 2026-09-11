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
        # code darret > 6
        # code derreur == 0
        self.dictMove = {
            'q': [1, 1],
            'w': [2, 0.9],
            'e': [3, 1],
            's': [4, 0.6],
            '.': [5, 0.05],
            ',': [6, -0.05],
            'space': [7, 0],
            'x': [8, 0]
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
        if code == 7: self.power = 0
        if code == 8: 
            print ("Program has been stop")
            self.run = False 
            self.power = 0

    # input: direction et vitesse
    # output: vitesse donnee
    def PowerServing(self, strike):
        if  strike[0] == 1 or strike == 3:
            self.power = strike[1]
        if strike[0] == 2 or strike[0] == 4 and self.power == 0:
            self.power = strike[1]
        if self.directAct == 2 or self.directAct == 4 and strike[0] == 5 or strike[0] == 6:
            self.power += strike[1]
            self.SendMSG(self.directAct)

    def ChooseMove(self, move):
        if move == 5 or move == 6 or move == 8:
            return
        else:
            self.directAct = move
        


    def SendMSG(self, move):
        gen_ev_externe(param.IP_ADRESS, self.port, move, self.power)

                

telecommande = telecom()
while telecommande.run:
    telecommande.SendMSG(telecommande.ReadKey())
    time.sleep(0.75)
    
    