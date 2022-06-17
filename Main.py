# https://github.com/opencv/opencv/issues/17687#issuecomment-872291073
# Komischer Workaround, damit die Kamera nicht 30 Sekunden zum Initialisieren braucht
# MUSS vor "import cv2" stehen.
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import GlobalShared
import GUIManager
import PictureProcessor


# Main-Methode, die dafür sorgt, dass alles instantiiert wird
if __name__ == '__main__':
    # initialisiert die Kamera dem Betriebssystem entsprechend
    pp = PictureProcessor.PictureProcessor()
    pp.initiateCapture()

    # Teilen des PictureProcessors mit allen
    GlobalShared.pictureProcessor = pp

    # Initialisiert die GUI
    gui = GUIManager.GUIManager()
    gui.run()
