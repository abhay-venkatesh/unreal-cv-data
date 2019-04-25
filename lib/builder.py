from PIL import Image
from io import BytesIO
from pathlib import Path
from tqdm import tqdm
from unrealcv import client
import os
import random
import time


class Builder:
    PITCH = 270
    ROLL = 0
    Z_COORD = 2500
    X_RANGE = 18000
    Y_RANGE = 14000

    def __init__(self, environment_folder):
        self.dataset_dir = Path(environment_folder, "dataset")
        self.images_folder = Path(self.dataset_dir, "images")
        self.masks_folder = Path(self.dataset_dir, "masks")
        paths = [self.dataset_dir, self.images_folder, self.masks_folder]
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def build(self, length):
        print("Building dataset...")
        for i in tqdm(range(length)):
            self._capture_mask(i)

    def _capture_mask(self, i):
        x = random.uniform(-self.X_RANGE, self.X_RANGE)
        y = random.uniform(-self.Y_RANGE, self.Y_RANGE)
        yaw = random.uniform(0, 360)
        self._capture(x, y, yaw, i)

    def _capture(self, x, y, yaw, i):
        client.request(('vset /camera/0/location {x} {y} {z}').format(
            x=x, y=y, z=self.Z_COORD))
        client.request(('vset /camera/0/rotation {pitch} {yaw} {roll}').format(
            pitch=self.PITCH, yaw=yaw, roll=self.ROLL))

        time.sleep(1)

        lit = client.request('vget /camera/0/lit png')
        lit_img = Image.open(BytesIO(lit))
        lit_img.save(Path(self.images_folder, str(i) + ".png"))

        time.sleep(1)

        mask = client.request('vget /camera/0/object_mask png')
        mask_img = Image.open(BytesIO(mask))
        mask_img.save(Path(self.masks_folder, str(i) + ".png"))

    def get_random_points(self, count):
        return [self._get_random_point() for _ in range(count)]

    def build_from_points(self, points):
        for i, point in tqdm(enumerate(points)):
            x, y, yaw = point
            self._capture(x, y, yaw, i)

    def _get_random_point(self):
        x = random.uniform(-self.X_RANGE, self.X_RANGE)
        y = random.uniform(-self.Y_RANGE, self.Y_RANGE)
        yaw = random.uniform(0, 360)
        return (x, y, yaw)
