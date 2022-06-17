import GlobalShared
from math import floor


##############################################
# top left    #   top center  #   top right  #
#   (0,2)     #     (1,2)     #    (2,2)     #
##############################################
# middle left #     center    # middle right #
#   (0,1)     #     (1,1)     #     (2,1)    #
##############################################
# bottom left # bottom center # bottom right #
#    (0,0)    #     (1,0)     #     (2,0)    #
##############################################
def positionDictionarySwitcher(i: tuple):
    positionDict = {
        (0, 0): "bottom left",
        (1, 0): "bottom center",
        (2, 0): "bottom right",
        (0, 1): "middle left",
        (1, 1): "center",
        (2, 1): "middle right",
        (0, 2): "top left",
        (1, 2): "top center",
        (2, 2): "top right"
    }
    return positionDict.get(i)


# Klasse, die die Berechnung der Positionen von Objekten durchführt.
class PositionHandler:

    def __init__(self):
        self.objectCoordinateDict = None
        self.recognizedObjects = None
        self.classIds = None

        self.pp = GlobalShared.pictureProcessor

        self.cameraWidth = self.pp.getResolutionX()
        self.cameraWidthThird = int(round(1 / 3 * self.cameraWidth))
        self.cameraHeight = self.pp.getResolutionY()
        self.cameraHeightThird = int(round(1 / 3 * self.cameraHeight))

    # Holt sich zunächst alle Objekte und ihre Koordinaten aus dem GlobalShared.objectCoordinateDict.
    # Dann wird die aktuelle Kameraauflösung abgerufen und ihre Breite und Höhe jeweils durch drei dividiert.
    # Die Koordinaten werden dann durch ein Drittel der Kamera-Breite und -Höhe dividiert und abgerundet, sodass
    # Werte im Intervall von [0,2] entstehen können. Diese Werte werden als Tupel in positionDictionarySwitcher gegeben
    # und in natürlichsprachige Positionen konvertiert. Am Ende wird alles in objectCoordinateDict gepackt und
    # zurückgegeben, sodass TTS daraus Sätze bilden kann.
    def calculatePositions(self):
        self.objectCoordinateDict = GlobalShared.objectCoordinateDict

        self.cameraWidth = int(round(self.pp.getResolutionX()))
        self.cameraWidthThird = int(round(1 / 3 * self.cameraWidth))
        self.cameraHeight = int(round(self.pp.getResolutionY()))
        self.cameraHeightThird = int(round(1 / 3 * self.cameraHeight))

        for k in self.objectCoordinateDict:
            v = self.objectCoordinateDict.get(k)
            coordinateX = floor(v[0] / self.cameraWidthThird)
            coordinateY = floor(v[1] / self.cameraHeightThird)
            positionTuple = positionDictionarySwitcher((coordinateX, coordinateY))
            self.objectCoordinateDict.update({k: positionTuple})
        return self.objectCoordinateDict
