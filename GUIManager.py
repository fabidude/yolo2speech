#########################################################################################
# https://github.com/opencv/opencv/issues/17687#issuecomment-872291073
# Komischer Workaround, damit die Kamera nicht 30 Sekunden zum Initialisieren braucht
# MUSS vor "import cv2" stehen.
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
#########################################################################################
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
from kivy.logger import Logger


class GUIManager(App):

    def __init__(self, **kwargs):
        App.__init__(self)
        self.resolutionButton = None
        self.resolutionsIndex = 1

        # Image-Widget für die Kamera
        self.img = Image()
        self.capture = None
        self.pp = PictureProcessor()


    # Baut die App:
    # Erstellt die Widgets und fügt sie dem Layout zu
    def build(self):

        # https://kivy.org/doc/stable/api-kivy.uix.pagelayout.html#module-kivy.uix.pagelayout
        layout = PageLayout()

        # https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#module-kivy.uix.gridlayout
        griddy = GridLayout(cols=3, spacing=5, row_force_default=True, row_default_height=50, orientation='lr-bt')

        # Kamerabild und das Grid-Layout hinzufügen
        layout.add_widget(self.img)
        layout.add_widget(griddy)

        # Findet die Kamera mit cv2
        self.pp.initiateCapture()

        # 9 Togglebutton-Dummies auf Seite 2 hinzufügen
        # Werden von unten nach oben und links nach rechts hinzugefügt
        griddy.add_widget(ToggleButton(text='Sprachausgabe ein / aus'))
        griddy.add_widget(ToggleButton(text='Kästen zeigen'))

        # Button, der die Auflösung ändert
        self.resolutionButton = Button(text=
                                  f'Auflösung ändern \n {int(self.pp.getResolutionX())}'
                                  f' x {int(self.pp.getResolutionY())}')
        griddy.add_widget(self.resolutionButton)

        # Binden der Callback-Funktion
        self.resolutionButton.bind(on_press=self.changeResolutionCallback)

        griddy.add_widget(ToggleButton(text='Yolo-V5'))
        griddy.add_widget(ToggleButton(text='Yolo-R'))
        griddy.add_widget(ToggleButton(text='Yolo-X'))
        griddy.add_widget(Label(text='Optionen'))

        # Definiert das Intervall, das bestimmt, wie häufig update() aufgerufen wird.
        # Equivalent zu Bildern pro Sekunde (1/25).
        Clock.schedule_interval(self.update, 1.0 / 25.0)
        return layout

    # Wird in build() per Clock-Intervall aufgerufen.
    # Aktualisiert das Webcam-Bild alle 1/25 Sekunden.
    def update(self, dt):
        # Kamerabild abgreifen
        ret, frame = self.pp.capture.read()

        # Flipt das Bild auf den Kopf, ansonsten wäre es falsch herum
        bildPuffer = cv2.flip(frame, 0)

        try:
            # Umwandlung in Bytes. Wirft AttributeError, falls Kamera
            # von anderer Anwendung verwendet oder nicht verbunden
            bildPufferBytes = bildPuffer.tobytes()

            # Umwandlung von Bild in Textur für Kivy
            textur = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

            # https://kivy.org/doc/stable/api-kivy.graphics.texture.html#kivy.graphics.texture.Texture.blit_buffer
            textur.blit_buffer(bildPufferBytes, colorfmt='bgr', bufferfmt='ubyte')

            # Bild aus Textur darstellen.
            self.img.texture = textur

        except AttributeError:
            Logger.error("Fehler: Kamera wird von anderer Anwendung verwendet oder nicht verbunden!")
            GUIManager.stop(self)

    # Callback-Funktion, die die Auflösung ändert
    def changeResolutionCallback(self, instance):
        resolutions = [[640, 480], [800, 600], [1280, 720], [1920, 1080]]
        if self.resolutionsIndex >= len(resolutions):
            self.resolutionsIndex = 0
        self.pp.capture.release()
        self.pp.initiateCapture()
        self.pp.setResolution(self.pp.capture, resolutions[self.resolutionsIndex])
        self.resolutionButton.text = f'Auflösung ändern \n {int(self.pp.getResolutionX())} x {int(self.pp.getResolutionY())}'
        Logger.info(f'Auflösung neu: {self.pp.getResolutionX()} x {self.pp.getResolutionY()}')
        self.resolutionsIndex += 1


if __name__ == '__main__':
    GUIManager().run()
    cv2.destroyAllWindows()
