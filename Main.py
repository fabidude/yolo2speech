# Wichtig: Es muss vorher Visual Studio mit den Funktionen "Python-Entwicklung", ".NET Multi-Plattform App UI-Entwicklung",
# ".NET Desktop-Entwicklung" und "Desktop Development with C++" installiert werden. 
# Dann zudem "pip install torch protobuf onnx onnxruntime==1.19.0 yolox==0.3.0 --no-deps loguru pycocotools tabulate kivy gtts pygame typing_extensions" 

# Komischer Workaround, damit die Kamera nicht 30 Sekunden zum Initialisieren braucht
# MUSS vor "import cv2" stehen.
# https://github.com/opencv/opencv/issues/17687#issuecomment-872291073
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
