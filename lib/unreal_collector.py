from lib.preprocessor import PreProcessor
from lib.builder import Builder
from pathlib import Path
import os


class UnrealCollector:
    def __init__(self, environment_name):
        self.environment_name = environment_name
        self.environment_folder = Path("environments", self.environment_name)
        paths = [
            Path("environments"),
            self.environment_folder,
        ]
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def collect(self):
        # First we prepare the Unreal Engine environment by preprocessing it
        PreProcessor(self.environment_folder).preprocess()

        # Then we build our dataset
        Builder(self.environment_folder).build(400)