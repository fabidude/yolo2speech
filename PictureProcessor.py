from platform import system, release
import cv2


# Differenziert zwischen den Betriebssystemen, da sie verschiedene
# Videoquellen für die Kamera nutzen
# https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga023786be1ee68a9105bf2e48c700294d
betriebsSystemName = system()

if betriebsSystemName == "Windows":
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif betriebsSystemName == "Linux":
    capture = cv2.VideoCapture(0, cv2.CAP_V4L)
elif betriebsSystemName == "Darwin":                    # MacOS
    capture = cv2.VideoCapture(0, cv2.CAP_QT)           # QuickTime
else:
    capture = cv2.VideoCapture(0, cv2.CAP_ANY)
print(f'{betriebsSystemName} ' + release())


def getResolutionY():
    height = capture.get(4)
    print(f'Height: {height}')
    return height


def getResolutionX():
    width = capture.get(3)
    print(f'Width: {width}')
    return width
