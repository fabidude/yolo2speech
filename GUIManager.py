import cv2
import PictureProcessor

from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from kivy.logger import Logger


class GUIManager(App):
    # Baut die App
    def build(self):
        # Erstellt die Widgets und fügt sie dem Layout zu

        # Image-Widget für die Kamera
        self.img = Image()

        # https://kivy.org/doc/stable/api-kivy.uix.pagelayout.html#module-kivy.uix.pagelayout
        layout = PageLayout()

        # https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#module-kivy.uix.gridlayout
        griddy = GridLayout(cols=3)

        # Kamerabild und das Grid-Layout hinzufügen
        layout.add_widget(self.img)
        layout.add_widget(griddy)

        # 9 Togglebutton-Dummies auf Seite 2 hinzufügen
        for i in range(9):
            iStr = f'Option {str(i + 1)}'
            griddy.add_widget((ToggleButton(text=iStr)))

        # Findet die Kamera mit cv2
        self.capture = PictureProcessor.capture

        # Definiert das Intervall, das bestimmt, wie häufig update() aufgerufen wird.
        # Equivalent zu Bildern pro Sekunde (1/25).
        Clock.schedule_interval(self.update, 1.0 / 25.0)
        return layout

    # Wird in build() per Clock-Intervall aufgerufen.
    # Aktualisiert das Webcam-Bild alle 1/25 Sekunden.
    def update(self, dt):
        # Kamerabild abgreifen
        ret, frame = self.capture.read()

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


if __name__ == '__main__':
    GUIManager().run()
    cv2.destroyAllWindows()
