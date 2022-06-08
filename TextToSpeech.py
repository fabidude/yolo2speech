from time import sleep

import gtts
import os

# fab: Wird benötigt um zu prüfen, ob neue Objekte in GlobalShared.classIds sind
from kivy.clock import Clock

from pygame import mixer

from yolox.data.datasets import COCO_CLASSES
from kivy.logger import Logger as logger

import GlobalShared
from GlobalShared import classIds


class TextToSpeech:
    def __init__(self):
        self.tts = None
        self.classIds = None
        self.recognizedObjects = None
        mixer.init()
        # Clock.schedule_interval(self.ablauf, 1.0)

    def ablauf(self):
        print("initiated")
        print(self.recognizedObjects)
        self.getObjects()
        for index, object in enumerate(self.recognizedObjects):
            logger.info(f"Objekt: {object}")
            self.generateSpeechFile(object)
            self.playSpeechFile(object)
            if index == len(self.recognizedObjects):
                self.recognizedObjects = []
            sleep(1)
            # self.deleteSpeechFile(i)
        print("done")

    def generateSpeechFile(self, text):
        self.tts = gtts.gTTS(text, lang='en')
        self.tts.save(f'./audio/{text}.mp3')

    def deleteSpeechFile(self, text):
        os.remove(f'./audio/{text}.mp3')

    def playSpeechFile(self, text):
        mixer.music.load(f'./audio/{text}.mp3')
        mixer.music.play()

    # fab: Holt sich alle erkannten Objekte aus GlobalShared.classIds
    def getObjects(self):
        self.classIds = GlobalShared.classIds
        self.recognizedObjects = []

        for i in classIds:
            if COCO_CLASSES[i] not in self.recognizedObjects:
                self.recognizedObjects.append(COCO_CLASSES[i])


# if __name__ == '__main__':
#     tts = TextToSpeech()

''' Ausprobieren:
tt = TextToSpeech()
texty = "Hier einen Testtext eingeben!"
tt.generateSpeechFile(texty)
tt.playSpeechFile()
tt.deleteSpeechFile()
'''
