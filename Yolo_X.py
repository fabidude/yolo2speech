# Igor: Die Datei basiert auf der Datei: YOLOX/tools/demo.py

import time
import torch

from yolox.data.data_augment import ValTransform
from yolox.data.datasets import COCO_CLASSES
from yolox.exp import get_exp
from yolox.utils import get_model_info, postprocess

import GlobalShared
from visualize import *

from kivy.logger import Logger as logger

"""

Die Predictor-Klasse ist ein Objekt, dass die Methoden für die Berechnung der
Inferenz und die Darstellung der Bounding-Boxes bereitstellt.
"""


class Predictor(object):
    def __init__(
            self,
            model,
            exp,
            cls_names=COCO_CLASSES,
            decoder=None,
            device="cpu",
            fp16=False,
            legacy=False,

    ):
        self.model = model
        self.cls_names = cls_names
        self.decoder = decoder
        self.num_classes = 80
        self.confthre = 0.45
        self.nmsthre = 0.65
        self.test_size = (640, 640)
        self.device = device
        self.fp16 = fp16
        self.preproc = ValTransform(legacy=legacy)
        self.exp = get_exp(None, "yolox-nano")

    # Berechnung der Inferenz. Hier geschieht der ganze ML-Spaß.
    def inference(self, img):
        img_info = {"id": 0, "raw_img": img}

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
            # Kann man wieder aktivieren, wenn man die infer time wissen will
            # logger.info("Infer time: {:.4f}s".format(time.time() - t0))
        return outputs, img_info

    # Fügt das Bild wieder zusammen, inklusive Bounding Boxes
    def visual(self, output, img_info, cls_conf=0.35):
        ratio = img_info["ratio"]
        img = img_info["raw_img"]
        if output is None:
            return img
        output = output.cpu()

        bboxes = []

        if GlobalShared.showBoundingBoxes:
            bboxes = output[:, 0:4]

            # preprocessing: resize
            bboxes /= ratio
        if not GlobalShared.showBoundingBoxes:
            bboxes.clear()

        cls = output[:, 6]

        # Die erzielten Ergebnisse
        scores = output[:, 4] * output[:, 5]

        vis_res = vis(img, bboxes, scores, cls, cls_conf, self.cls_names)
        return vis_res


# Methode, um den YOLOX-Predictor herzustellen
def makePredictor():
    exp = get_exp(None, "yolox-nano")
    print(exp)
    model = exp.get_model()
    logger.info(f"Model Summary: {get_model_info(model, exp.test_size)}")
    device = "cpu"
    model.eval()

    # laden des checkpoints
    ckpt_file = "./YOLOX/yolox_nano.pth"

    logger.info(f"loading checkpoint {ckpt_file}")
    ckpt = torch.load(ckpt_file, map_location="cpu")
    # load the model state dict
    model.load_state_dict(ckpt["model"])
    logger.info("loading checkpoint done.")
    trt_file = None
    decoder = None

    return Predictor(model, exp, COCO_CLASSES, trt_file, decoder, device)
