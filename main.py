from importlib import import_module as im

if __name__ == "__main__":
    """ Uncomment the tool you are interested in """

    # im("toolbox.collect").collect("modular_neighborhood")
    # im("toolbox.build_default_dataset").build()
    im("toolbox.find_class").find_class(rgba="(R=191,G=0,B=223,A=255)")
