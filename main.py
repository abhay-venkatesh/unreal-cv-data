from importlib import import_module as im

if __name__ == "__main__":
    """ Uncomment the tool you are interested in """

    """
    im("lib.unreal_collector").UnrealCollector("modular_neighborhood").collect(
        count=4000)
    """
    # im("toolbox.build_testing_dataset").build()
    # im("toolbox.build_default_dataset").build()
    im("toolbox.find_class").find_class(rgba="(R=0,G=255,B=0,A=255)")
