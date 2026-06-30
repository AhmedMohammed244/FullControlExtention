from modules.input_loader import InputLoader

class Pipeline:

    def __init__(self):
        self.loader = InputLoader()

    def run(self, source):

        task = self.loader.load(source)

        return task