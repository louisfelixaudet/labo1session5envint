import cv2
import platform
import os

class CameraWindows:
    def __init__(self, largeur = 320, hauteur = 240):
        self.largeur = largeur
        self.hauteur = hauteur

    def capture(self):
        ret, image = self.vcap.read() 
        return image

    def demarrer(self):
        if platform.system() == "Windows":
            self.vcap = cv2.VideoCapture(0)
            self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, self.largeur)
            self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.hauteur)


    def arreter(self):
       self.vcap.release()

class CameraLinux:
    def __init__(self, largeur = 320, hauteur = 240):
        if platform.system() == "Linux":
            from picamera2 import Picamera2
            self.picam2 = Picamera2()
            config = picam2.create_video_configuration(main={"format": 'RGB888', "size": (largeur, hauteur)})
            self.picam2.configure(config) 

    def capture(self):
        image = self.picam2.capture_array()
        return image

    def demarrer(self):
        self.picam2.start() 


    def arreter(self):
       self.picam2.stop()

class Camera:
    def __init__(self, largeur = 320, hauteur = 240):
        if platform.system() == "Linux":
            self.cam = CameraLinux(largeur, hauteur)
        if platform.system() == "Windows":
            self.cam = CameraWindows(largeur, hauteur)

    def capture(self):
        return self.cam.capture()

    def demarrer(self):
        self.cam.demarrer() 


    def arreter(self):
       self.cam.arreter()
        
if __name__ == "__main__":
    terminer = False
    cam = Camera()
    cam.demarrer()

    while not terminer:
        cv2.imshow("image", cam.capture())
        choix = cv2.waitKey(30)
        if choix == ord('x'):
            terminer = True
