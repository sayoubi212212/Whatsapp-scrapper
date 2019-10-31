from pygame import mixer
import time
import threading
from Consts import *
import os


class SoundPlayer:
    def __init__(self, mp3):
        mixer.init()
        mixer.music.load(mp3)

    def play(self):
        def playSound():
            mixer.music.play(0)
            time.sleep(3)
        t = threading.Thread(target=playSound, args=())
        t.start()

