from PyQt5.QtTextToSpeech import *

class TTS:
    def __init__(self):
        self.engine = QTextToSpeech()
    def text_to_speech(self, text, sts=True):
        if sts:
            self.engine.say(str(text))
        return