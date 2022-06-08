from platform import system
import cv2


class PictureProcessor:
    capture = None

    def __init__(self):
        self

    """
    fab:
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
            self.capture = cv2.VideoCapture(0, cv2.CAP_QT)  # fab: QuickTime. Bin mir nicht sicher, ob das richtig ist.
        else:
            self.capture = cv2.VideoCapture(0, cv2.CAP_ANY)

    # fab: Holt den aktuellen Kamera-Frame
    def getCameraFrame(self):
        ret, frame = self.capture.read()
        return [ret, frame]

    # fab: Gibt die vertikale Auflösung aus
    def getResolutionY(self):
        height = self.capture.get(4)
        return height

    # fab: Gibt die horizontale Auflösung aus
    def getResolutionX(self):
        width = self.capture.get(3)
        return width

    # fab: Gibt die Auflösung aus
    def getResolution(self):
        return self.capture.get(3), self.capture.get(4)

    # fab: Legt die Auflösung der Kamera fest
    def setResolution(self, capture, resolution):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
