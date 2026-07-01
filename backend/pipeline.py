from modules.input_loader import InputLoader
from modules.audio_info import AudioInfo


class Pipeline:

    def __init__(self):

        self.loader = InputLoader()

        self.audio_info = AudioInfo()

    def run(self, source):

        task = self.loader.load(source)

        task = self.audio_info.analyze(task)

        return task