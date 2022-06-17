import gtts
import os

from os.path import exists
from pygame import mixer

audioPath = "./audio/"

# Klasse, die Funktionen für Generierung, Abspielen und Löschen eines Speechfiles bereitstellt.
class TextToSpeech:
    def __init__(self):
        self.ph = None
        self.tts = None
        self.classIds = None
        self.recognizedObjects = None
        self.outputString = ""
        self.mixer = mixer
        self.mixer.init()

    # Ablauf: Falls eine output.mp3 in ./audio/ existiert, wird sie zunächst gelöscht.
    # Outputstring wird generiert mit "n objects recognized", wobei n die Menge der erkannten Objekte ist.
    # Dann wird recognizedObjects (dict) durchgegangen und an den Outputstring konkateniert.
    # Aus dem Outputstring wird dann eine output.mp3 generiert und abgespielt.
    def main(self, recognizedObjects):
        if exists(f'{audioPath}output.mp3'):
            self.deleteSpeechFile()

        self.outputString = ""
        self.outputString += f"{len(recognizedObjects)} objects recognized."

        for k in recognizedObjects:
            v = recognizedObjects.get(k)
            self.outputString += f" {k, v},"

        self.generateSpeechFile(self.outputString)
        print(f"Output: {self.outputString}")

        self.playSpeechFile()

    def generateSpeechFile(self, text):
        self.tts = gtts.gTTS(text, lang='en')
        self.tts.save(f'{audioPath}output.mp3')

    def deleteSpeechFile(self):
        self.mixer.quit()
        os.remove(f'{audioPath}output.mp3')

    def playSpeechFile(self):
        self.mixer.init()
        self.mixer.music.load(f'{audioPath}output.mp3')
        self.mixer.music.play()
