from unrealcv import client

if __name__ == "__main__":
    client.connect()
    if not client.isconnected():
        raise RuntimeError("Could not connect to client. ")

    client.request('vset /camera/0/location 4400 4500 2100')
    client.request('vset /camera/0/rotation 270 180 0')

    # Fix pitch, roll, z
    # client.request('vset /camera/0/location {x} {y} {z}')
    # client.request('vset /camera/0/rotation {pitch} {yaw} {roll}')



# location = client.request('vget /camera/0/location')
# orientation = client.request('vget /camera/0/rotation')
# print(location, orientation)
# 4344.432 4542.351 2113.637 270.100 179.243 0.000
