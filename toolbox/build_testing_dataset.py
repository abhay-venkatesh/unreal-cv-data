from lib.preprocessor import PreProcessor
from lib.builder import Builder


def build():
    environment_folder = "testing"
    builder = Builder(environment_folder)
    points = builder.get_random_points(400)
    builder.build_from_points(points)
    preprocessor = PreProcessor(environment_folder)
    preprocessor.preprocess()
    builder.build_from_points(points)