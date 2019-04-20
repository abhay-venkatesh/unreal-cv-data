from lib.builder import Builder
from lib.preprocessor import PreProcessor
from lib.unreal_collector import UnrealCollector
from unrealcv import client


def build():
    default_environment_folder = UnrealCollector(
        "testing_default").environment_folder

    client.connect()
    if not client.isconnected():
        raise RuntimeError("Could not connect to client. ")

    builder = Builder(default_environment_folder)
    points = builder.get_random_points(400)
    builder.build_from_points(points)

    new_environment_folder = UnrealCollector("testing_new").environment_folder
    builder = Builder(new_environment_folder)
    PreProcessor(new_environment_folder).preprocess()
    builder.build_from_points(points)

    client.disconnect()