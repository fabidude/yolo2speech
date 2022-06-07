import GUIManager
import Yolo_X
import PictureProcessor
import GlobalShared
from yolox.exp import get_exp

if __name__ == '__main__':
    pp = PictureProcessor.PictureProcessor()
    pp.initiateCapture()
    GlobalShared.currentRet, GlobalShared.currentFrame = pp.getCameraFrame()

    GlobalShared.predictor = Yolo_X.makePredictor()

    gui = GUIManager.GUIManager()
    gui.run()

