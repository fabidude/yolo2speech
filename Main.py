import GUIManager
import Yolo_X
import PictureProcessor
import GlobalShared
from yolox.exp import get_exp

if __name__ == '__main__':
    pp = PictureProcessor.PictureProcessor()
    pp.initiateCapture()

    GlobalShared.currentRet, GlobalShared.currentFrame = pp.getCameraFrame()

    Yolo_X.makePredictor()
    predictor = GlobalShared.predictor  # holt den Prediktor als globale Variable

    outputs, img_info = predictor.inference(GlobalShared.currentFrame)
    GlobalShared.currentFrame = predictor.visual(outputs[0], img_info, predictor.confthre)

    gui = GUIManager.GUIManager()

    # while True:
        # print(GlobalShared.currentRet)
        # outputs, img_info = predictor.inference(GlobalShared.currentFrame)
        # GlobalShared.currentFrame = predictor.visual(outputs[0], img_info, predictor.confthre)
        # gui.update()
