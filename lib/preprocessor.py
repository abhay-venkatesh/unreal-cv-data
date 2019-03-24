from pathlib import Path
from tqdm import tqdm
from unrealcv import client
import json
import re


class Color(object):
    ''' A utility class to parse color value '''
    regexp = re.compile('\(R=(.*),G=(.*),B=(.*),A=(.*)\)')  # noqa W605

    def __init__(self, color_str):
        self.color_str = color_str
        match = self.regexp.match(color_str)
        (self.R, self.G, self.B,
         self.A) = [int(match.group(i)) for i in range(1, 5)]

    def __repr__(self):
        return self.color_str


class PreProcessor:
    def __init__(self, dest_dir):
        self.dest_dir = dest_dir

    def preprocess(self):
        self._get_colors()

    def _get_colors(self):
        client.connect()
        if not client.isconnected():
            raise RuntimeError("Could not connect to client. ")

        scene_objects = client.request('vget /objects').split(' ')
        print('Number of objects in this scene:', len(scene_objects))

        colors = dict()
        for scene_obj in tqdm(scene_objects):
            request_str = "vget /object/" + scene_obj + "/color"
            colors[scene_obj] = client.request(request_str)
        with open(Path(self.dest_dir, "colors.json"), 'w') as fp:
            json.dump(colors, fp)
