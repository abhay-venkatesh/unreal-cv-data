from lib.builder import Builder
from lib.preprocessor import PreProcessor
from pathlib import Path
from unrealcv import client
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

    def collect(self, count=400, preprocess=True):
        client.connect()
        if not client.isconnected():
            raise RuntimeError("Could not connect to client. ")

        # First we prepare the Unreal Engine environment by preprocessing it
        if preprocess:
            PreProcessor(self.environment_folder).preprocess()

        # Then we build our dataset
        Builder(self.environment_folder).build(count)

        client.disconnect()

    def get_obj_from_color(self, color):
        pp = PreProcessor(self.environment_folder)
        return pp.get_obj_from_color(color)

    def condense_colors(self):
        pp = PreProcessor(self.environment_folder)
        pp.condense_colors()
