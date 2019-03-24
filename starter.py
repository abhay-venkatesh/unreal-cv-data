from unrealcv import client
import time
import sys

print(
    time.strftime("The last update of this file: %Y-%m-%d %H:%M:%S",
                  time.gmtime()))

# Establish the connection with the UE4 game

client.connect()
if not client.isconnected():
    print(
        'UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.'
    )
    sys.exit(-1)

# Checking status of the connection between UnrealCV and UE4 game

res = client.request('vget /unrealcv/status')
# The image resolution and port is configured in the config file.
print(res)
