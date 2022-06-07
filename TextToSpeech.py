import gtts
import os
from playsound import playsound
from GlobalShared import classIds


class TextToSpeech:
    def __init__(self):
        pass

    def generateSpeechFile(self, text):
        tts = gtts.gTTS(text, lang='de')
        tts.save('testfile.mp3')

    def deleteSpeechFile(self):
        os.remove('testfile.mp3')

    def playSpeechFile(self):
        playsound('testfile.mp3')


''' Ausprobieren:
tt = TextToSpeech()
texty = "Hier einen Testtext eingeben!"
tt.generateSpeechFile(texty)
tt.playSpeechFile()
tt.deleteSpeechFile()
'''
