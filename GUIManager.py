"""
https://github.com/opencv/opencv/issues/17687#issuecomment-872291073
Komischer Workaround, damit die Kamera nicht 30 Sekunden zum Initialisieren braucht
MUSS vor "import cv2" stehen.
"""
import os

import Yolo_X
from TextToSpeech import TextToSpeech

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2

from PictureProcessor import PictureProcessor

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.pagelayout import PageLayout
from kivy.uix.image import Image

from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.app import App
from kivy.logger import Logger as logger

import GlobalShared  # igor: for the predictor as a global variable

"""
fab:
Die Klasse, die für die Darstellung der GUI verantwortlich ist.
"""


class GUIManager(App):

    def __init__(self, **kwargs):
        App.__init__(self)
        self.yoloButton = None
        self.boundingBoxButton = None
        self.textToSpeechButton = None
        self.resolutionButton = None
        self.capture = None
        self.resolutionsIndex = 1

        # fab: Image-Widget für die Kamera
        self.img = Image()

        self.pp = PictureProcessor()

    # fab: Baut die App.
    # Erstellt die Widgets und fügt sie dem Layout zu.
    def build(self):

        # fab: fab: https://kivy.org/doc/stable/api-kivy.uix.pagelayout.html#module-kivy.uix.pagelayout
        layout = PageLayout()

        # fab: https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#module-kivy.uix.gridlayout
        griddy = GridLayout(cols=4, spacing=5, row_force_default=True, row_default_height=50, orientation='lr-bt')

        # fab: Kamerabild und das Grid-Layout hinzufügen
        layout.add_widget(self.img)
        layout.add_widget(griddy)

        # fab: Findet die Kamera mit cv2
        self.pp.initiateCapture()

        ######################################
        # fab: Togglebuttons
        # Werden von unten nach oben und links nach rechts hinzugefügt (bt-lr)

        # textToSpeechButton
        self.textToSpeechButton = Button(text='Sprachausgabe')
        griddy.add_widget(self.textToSpeechButton)

        # boundingBoxButton
        self.boundingBoxButton = ToggleButton(text='Boundingboxes zeigen', state='down')
        griddy.add_widget(self.boundingBoxButton)

        self.yoloButton = ToggleButton(text='YoloX', state='normal')
        griddy.add_widget(self.yoloButton)

        # fab: Button, der die Auflösung ändert
        self.resolutionButton = Button(text=
                                       f'Auflösung ändern \n {int(self.pp.getResolutionX())}'
                                       f' * {int(self.pp.getResolutionY())}')
        griddy.add_widget(self.resolutionButton)

        # fab: Binden der Callback-Funktionen
        self.resolutionButton.bind(on_press=self.changeResolutionCallback)
        self.textToSpeechButton.bind(on_press=self.initiateTTSCallback)
        self.boundingBoxButton.bind(on_press=self.toggleBoundingBoxesCallback)
        self.yoloButton.bind(on_press=self.yoloButtonCallback)

        # fab: Optionen-Label
        griddy.add_widget(Label(text='Optionen'))

        # fab: Definiert das Intervall, das bestimmt, wie häufig update() aufgerufen wird.
        # Entsprechend zu Bildern pro Sekunde (1/25).
        Clock.schedule_interval(self.update, 1.0 / 25.0)

        return layout

    # fab: Wird in build() per Clock-Intervall aufgerufen.
    # Aktualisiert das Webcam-Bild alle 1/25 Sekunden.
    def update(self, dt):
        # fab: Kamerabild abgreifen
        ret, frame = self.pp.getCameraFrame()

        # igor: holt den Prediktor als globale Variable
        predictor = GlobalShared.predictor

        if ret:

            if GlobalShared.makePredictor:
                outputs, img_info = predictor.inference(frame)
                frame = predictor.visual(outputs[0], img_info, predictor.confthre)

            # fab: Flipt das Bild auf den Kopf, ansonsten wäre es falsch herum
            bildPuffer = cv2.flip(frame, 0)

            try:
                # fab: Umwandlung in Bytes. Wirft AttributeError, falls Kamera
                # von anderer Anwendung verwendet oder nicht verbunden
                bildPufferBytes = bildPuffer.tobytes()

                # fab: Umwandlung von Bild in Textur für Kivy
                textur = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

                # fab: https://kivy.org/doc/stable/api-kivy.graphics.texture.html#kivy.graphics.texture.Texture.blit_buffer
                textur.blit_buffer(bildPufferBytes, colorfmt='bgr', bufferfmt='ubyte')

                # fab: Bild aus Textur darstellen.
                self.img.texture = textur

            except AttributeError:
                logger.error("Fehler: Kamera wird von anderer Anwendung verwendet oder nicht verbunden!")
                GUIManager.stop(self)

    # fab: Callback-Funktion des resolutionButtons, die die Auflösung ändert.
    # Dauert aus einem mir unbekannten Grund extrem lange
    def changeResolutionCallback(self, instance):
        # fab: Zur Auswahl stehende Auflösungen
        resolutions = [[640, 480], [800, 600], [1280, 720], [1920, 1080]]

        if self.resolutionsIndex >= len(resolutions):
            self.resolutionsIndex = 0

        # fab: Released die Kamera und initiiert sie neu mit neuer Auflösung
        self.pp.capture.release()
        self.pp.initiateCapture()
        self.pp.setResolution(self.pp.capture, resolutions[self.resolutionsIndex])

        # fab: Ändert den Text des resolutionButtons zur aktuellen Auflösung
        self.resolutionButton.text = f'Auflösung ändern \n {int(self.pp.getResolutionX())} * {int(self.pp.getResolutionY())}'
        logger.info(f'Auflösung: {self.pp.getResolutionX()} * {self.pp.getResolutionY()}')

        self.resolutionsIndex += 1

    def initiateTTSCallback(self, dt):
        tts = TextToSpeech()
        tts.main()

    def toggleBoundingBoxesCallback(self, dt):
        if self.boundingBoxButton.state == 'down':
            GlobalShared.showBoundingBoxes = True
        elif self.boundingBoxButton.state == 'normal':
            GlobalShared.showBoundingBoxes = False
        # debug
        # print(self.boundingBoxButton.state, GlobalShared.showBoundingBoxes)

    def yoloButtonCallback(self, dt):
        if self.yoloButton.state == 'down':
            GlobalShared.predictor = Yolo_X.makePredictor()
            GlobalShared.makePredictor = True
        if self.yoloButton.state == 'normal':
            GlobalShared.predictor = None
            GlobalShared.makePredictor = False
