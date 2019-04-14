from lib.unreal_collector import UnrealCollector


def build():
    UnrealCollector("default").collect(preprocess=False)
