from lib.unreal_collector import UnrealCollector


def setup():
    # Comment the following line out when you are done setting up.
    # raise NotImplementedError("Please read setup() in main.py")

    # First, setup your Unreal Engine 4 environment,
    # Then, assign an environment name
    ENVIRONMENT_NAME = "modular_neighborhood"

    return ENVIRONMENT_NAME


if __name__ == "__main__":
    environment_name = setup()
    UnrealCollector(environment_name).collect()
