from unrealcv import client
client.connect()  # Connect to the game
if not client.isconnected(
):  # Check if the connection is successfully established
    print("UnrealCV server is not running. "
          "Run the game from http://unrealcv.github.io first. ")
else:
    filename = client.request('vget /camera/0/lit')
    filename = client.request('vget /camera/0/depth depth.exr')