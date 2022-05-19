from platform import system, release
from kivy.logger import Logger
import cv2


class PictureProcessor:
    capture = None

    def __init__(self):
        pass

    """
    Differenziert zwischen den Betriebssystemen, da sie verschiedene
    Videoquellen für die Kamera nutzen
    https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga023786be1ee68a9105bf2e48c700294d
    """
    def initiateCapture(self):
        if system() == "Windows":
            self.capture = cv2.VideoCapture(0, cv2.CAP_MSMF)
        elif system() == "Linux":
            self.capture = cv2.VideoCapture(0, cv2.CAP_V4L)
        elif system() == "Darwin":  # MacOS
            self.capture = cv2.VideoCapture(0, cv2.CAP_QT)  # QuickTime. Bin mir nicht sicher, ob das richtig ist.
        else:
            self.capture = cv2.VideoCapture(0, cv2.CAP_ANY)
        Logger.info(f'OS: {system()}{release()}')

    # Gibt die vertikale Auflösung aus
    def getResolutionY(self):
        height = self.capture.get(4)
        return height

    # Gibt die horizontale Auflösung aus
    def getResolutionX(self):
        width = self.capture.get(3)
        return width

    # Gibt die Auflösung aus
    def getResolution(self):
        return self.capture.get(3), self.capture.get(4)

    # Legt die Auflösung der Kamera fest
    def setResolution(self, capture, resolution):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
