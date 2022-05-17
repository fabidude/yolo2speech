from platform import system, release
from kivy.logger import Logger

import cv2

# Differenziert zwischen den Betriebssystemen, da sie verschiedene
# Videoquellen für die Kamera nutzen
# https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga023786be1ee68a9105bf2e48c700294d
betriebsSystemName = system()
if betriebsSystemName == "Windows":
    capture = cv2.VideoCapture(0, cv2.CAP_MSMF)
elif betriebsSystemName == "Linux":
    capture = cv2.VideoCapture(0, cv2.CAP_V4L)
elif betriebsSystemName == "Darwin":  # MacOS
    capture = cv2.VideoCapture(0, cv2.CAP_QT)  # QuickTime
else:
    capture = cv2.VideoCapture(0, cv2.CAP_ANY)
Logger.info(f'OS: {betriebsSystemName} ' + release())


def getResolutionY():
    height = capture.get(4)
    Logger.info(f'Bildhöhe: {height}')
    return height


def getResolutionX():
    width = capture.get(3)
    Logger.info(f'Bildbreite: {width}')
    return width


def setResolution(cam, x, y):
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, x)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, y)
