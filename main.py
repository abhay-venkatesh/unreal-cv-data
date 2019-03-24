from lib.unreal_collector import UnrealCollector
from unrealcv import client


def setup():
    # First, setup your Unreal Engine 4 environment,

    # Then, setup the config file using the following prompt
    # client.connect()
    # if not client.isconnected():
    #     raise RuntimeError("Could not connect to client. ")
    # print(client.request("vget /unrealcv/status"))
    # client.disconnect()

    # Then, assign an environment name
    ENVIRONMENT_NAME = "modular_neighborhood"

    # Comment the following line out when you are done setting up.
    # raise NotImplementedError("Please read setup() in main.py")

    return ENVIRONMENT_NAME


if __name__ == "__main__":
    environment_name = setup()
    UnrealCollector(environment_name).collect()
