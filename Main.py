import cv2

import GUIManager
import Yolo_X
import PictureProcessor
import GlobalShared
from TextToSpeech import TextToSpeech

"""
fab:
Main-Methode, die dafür sorgt, dass alles instantiiert wird
"""
if __name__ == '__main__':
    pp = PictureProcessor.PictureProcessor()

    # fab: initialisiert die Kamera dem Betriebssystem entsprechend
    pp.initiateCapture()

    # fab: Erschafft einen YOLOX-Predictor
    GlobalShared.predictor = Yolo_X.makePredictor()

    # fab: Initialisiert die GUI
    gui = GUIManager.GUIManager()
    gui.run()


