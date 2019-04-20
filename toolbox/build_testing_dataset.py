from lib.builder import Builder
from lib.preprocessor import PreProcessor
from lib.unreal_collector import UnrealCollector
from unrealcv import client


def build():
    environment_folder = UnrealCollector("testing").environment_folder

    client.connect()
    if not client.isconnected():
        raise RuntimeError("Could not connect to client. ")

    builder = Builder(environment_folder)
    points = builder.get_random_points(400)

    builder.build_from_points(points)
    PreProcessor(environment_folder).preprocess()
    builder.build_from_points(points)

    client.disconnect()