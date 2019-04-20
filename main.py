from importlib import import_module as im

if __name__ == "__main__":
    """ Uncomment the tool you are interested in """

    """
    im("lib.unreal_collector").UnrealCollector("modular_neighborhood").collect(
        count=4000)
    """
    im("toolbox.build_testing_dataset").build()
    # im("toolbox.build_default_dataset").build()
    # im("toolbox.find_class").find_class(rgba="(R=78,G=111,B=159,A=255)")
