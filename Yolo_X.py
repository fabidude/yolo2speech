# Igor: Die Datei basiert auf der Datei: YOLOX/tools/demo.py

import os
import time
import cv2
import torch
import GUIManager  # igor: import des GUIManagers
import GlobalShared  # igor: for the predictor as a global variable

from yolox.data.data_augment import ValTransform
from yolox.data.datasets import COCO_CLASSES
from yolox.exp import get_exp
from yolox.utils import fuse_model, get_model_info, postprocess, vis

from kivy.logger import Logger as logger


class Predictor(object):
    def __init__(
            self,
            model,
            exp,
            cls_names=COCO_CLASSES,
            decoder=None,
            device="gpu",
            fp16=False,
            legacy=False,

    ):
        self.model = model
        self.cls_names = cls_names
        self.decoder = decoder
        self.num_classes = 80
        self.confthre = 0.01
        self.nmsthre = 0.65
        self.test_size = (640, 640)
        self.device = device
        self.fp16 = fp16
        self.preproc = ValTransform(legacy=legacy)
        self.exp = get_exp(None, "yolox-nano")

    def inference(self, img):
        img_info = {"id": 0, "raw_img": img}
        # if isinstance(img, str):
        #     img_info["file_name"] = os.path.basename(img)
        #     img = cv2.imread(img)
        # else:
        #     img_info["file_name"] = None
        #
        # height, width = img.shape[:2]
        # img_info["height"] = height
        # img_info["width"] = width

        ratio = min(self.test_size[0] / img.shape[0], self.test_size[1] / img.shape[1])
        img_info["ratio"] = ratio

        img, _ = self.preproc(img, None, self.test_size)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.float()
        if self.device == "gpu":
            img = img.cuda()
            if self.fp16:
                img = img.half()  # to FP16

        with torch.no_grad():
            t0 = time.time()
            outputs = self.model(img)
            if self.decoder is not None:
                outputs = self.decoder(outputs, dtype=outputs.type())
            outputs = postprocess(
                outputs, self.num_classes, self.confthre,
                self.nmsthre, class_agnostic=True
            )
            # fab: Kann man wieder aktivieren, wenn man die infer time wissen will
            # logger.info("Infer time: {:.4f}s".format(time.time() - t0))
        return outputs, img_info

    # Fügt das Bild wieder zusammen, inklusive Bounding Boxes
    def visual(self, output, img_info, cls_conf=0.35):
        ratio = img_info["ratio"]
        img = img_info["raw_img"]
        if output is None:
            return img
        output = output.cpu()

        bboxes = output[:, 0:4]

        # preprocessing: resize
        bboxes /= ratio

        cls = output[:, 6]
        scores = output[:, 4] * output[:, 5]

        vis_res = vis(img, bboxes, scores, cls, cls_conf, self.cls_names)
        return vis_res


def makePredictor():  # (exp)
    global predictor
    exp = get_exp(None, "yolox-nano")

    # fab: Akzeptiert nur Objekte, die mit einer confidence >n erkannt werden
    exp.test_conf = 0.45

    # test nms threshold
    exp.nmsthre = 0.45

    # Test Image Size
    exp.test_size = (640, 640)

    model = exp.get_model()
    logger.info(f"Model Summary: {get_model_info(model, exp.test_size)}")

    # if torch.cuda.is_available():
    #     model.cuda()
    #     device = "gpu"
    # else:
    #     device = "cpu"
    device = "cpu"
    model.eval()

    ckpt_file = "./YOLOX/yolox_nano.pth"
    logger.info(f"loading checkpoint {ckpt_file}")
    ckpt = torch.load(ckpt_file, map_location="cpu")
    # load the model state dict
    model.load_state_dict(ckpt["model"])
    logger.info("loading checkpoint done.")
    trt_file = None
    decoder = None

    # igor: der Predictor wird als globale Variable (in GlobalShared.py) gesetzt.
    # In der main() wird also "predictor" mit "GlobalShared.predictor" ersetzt
    return Predictor(
        model, exp, COCO_CLASSES, trt_file, decoder, device
    )

    # gui = GUIManager.GUIManager()
    # gui.run()

# if __name__ == "__main__":
#     exp = get_exp(None, "yolox-nano")
#
#     main(exp)
