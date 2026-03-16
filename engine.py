import os
import random
from pygame import mixer

class TabataEngine:
    def __init__(self):
        mixer.init()

    def play_audio(self, file_path):
        if file_path and os.path.exists(file_path):
            mixer.music.load(file_path)
            mixer.music.play(-1)
        else:
            print(f"DEBUG: File audio tidak ditemukan di {file_path}")

    def stop_audio(self):
        if mixer.music.get_busy():
            mixer.music.stop()