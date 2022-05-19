import gtts
import os
from playsound import playsound


class TextToSpeech:
    def __init__(self):
        pass

    def generateSpeechFile(self, text):
        tts = gtts.gTTS(text, lang='de')
        tts.save(f'{text}.mp3')

    def deleteSpeechFile(self, file):
        os.remove(f'{file}.mp3')

    def playSpeechFile(self, file):
        playsound(f'{file}.mp3')

'''
Ausprobieren:
tt = TextToSpeech()
texty = "Hier einen Testtext eingeben!"
tt.generateSpeechFile(texty)
tt.playSpeechFile(texty)
tt.deleteSpeechFile(texty)
'''
