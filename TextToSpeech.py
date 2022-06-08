from time import sleep

import gtts
import os

# fab: Wird benötigt um zu prüfen, ob neue Objekte in GlobalShared.classIds sind
# from kivy.clock import Clock

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

    def main(self):
        self.getObjects()
        print(f"{len(self.recognizedObjects)} Objekt(e) erkannt: ")
        for index, object in enumerate(self.recognizedObjects):
            print(f"{index + 1}. {object}")
            self.generateSpeechFile(object)
            self.playSpeechFile(object)
            sleep(1)

            if index+1 == len(self.recognizedObjects):
                self.recognizedObjects.clear()
                GlobalShared.classIds.clear()


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

        for index in classIds:
            if COCO_CLASSES[index] not in self.recognizedObjects:
                self.recognizedObjects.append(COCO_CLASSES[index])
