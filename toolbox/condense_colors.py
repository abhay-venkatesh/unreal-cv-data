from lib.unreal_collector import UnrealCollector


def condense_colors(environment_name):
    uc = UnrealCollector(environment_name)
    uc.condense_colors()