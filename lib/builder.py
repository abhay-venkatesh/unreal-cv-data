from pathlib import Path
import os
import random
from unrealcv import client
from PIL import Image
from io import BytesIO
from tqdm import tqdm


class Builder:
    PITCH = 270
    ROLL = 0
    Z_COORD = 2500
    X_RANGE = 18000
    Y_RANGE = 14000

    def __init__(self):
        self.dataset_dir = Path("dataset")
        if not os.path.exists(self.dataset_dir):
            os.mkdir(self.dataset_dir)

    def build(self, length):
        client.connect()
        if not client.isconnected():
            raise RuntimeError("Could not connect to client. ")

        for i in tqdm(range(length)):
            self._capture_mask(i)

        client.disconnect()

    def _capture_mask(self, i):
        x = random.uniform(-self.X_RANGE, self.X_RANGE)
        y = random.uniform(-self.Y_RANGE, self.Y_RANGE)
        yaw = random.uniform(0, 360)
        client.request(('vset /camera/0/location {x} {y} {z}').format(
            x=x, y=y, z=self.Z_COORD))
        client.request(('vset /camera/0/rotation {pitch} {yaw} {roll}').format(
            pitch=self.PITCH, yaw=yaw, roll=self.ROLL))

        lit = client.request('vget /camera/0/lit png')
        lit_img = Image.open(BytesIO(lit))
        lit_img.save(Path(self.dataset_dir, "images", str(i) + ".png"))

        mask = client.request('vget /camera/0/object_mask png')
        mask_img = Image.open(BytesIO(mask))
        mask_img.save(Path(self.dataset_dir, "masks", str(i) + ".png"))