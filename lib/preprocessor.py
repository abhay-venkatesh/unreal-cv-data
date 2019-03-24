from pathlib import Path
from tqdm import tqdm
from unrealcv import client
import json
import os
import re
import csv
"""
Have:
object_id -> colors

Want:
object_id -> class
class -> color

How to:
1. Build obj_to_class 

"""


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
        self.dest_dir = Path(dest_dir, "json")
        self.obj_to_colors_file = Path(self.dest_dir, "obj_to_colors.json")
        # self.classes_file = Path(self.dest_dir, "classes.csv")
        self.obj_to_class_file = Path(self.dest_dir, "obj_to_class.json")

    def preprocess(self):
        if not os.path.exists(self.obj_to_colors_file):
            self._get_colors()
        self._build_obj_to_class()

    def _get_colors(self):
        client.connect()
        if not client.isconnected():
            raise RuntimeError("Could not connect to client. ")

        scene_objects = client.request('vget /objects').split(' ')
        print('Number of objects in this scene:', len(scene_objects))

        colors = {}
        for scene_obj in tqdm(scene_objects):
            request_str = "vget /object/" + scene_obj + "/color"
            colors[scene_obj] = client.request(request_str)
        with open(self.colors_file, 'w') as fp:
            json.dump(colors, fp)

        client.disconnect()

    def _build_obj_to_class(self):
        with open(self.obj_to_colors_file) as json_file:
            obj_to_colors = json.load(json_file)

        with open(Path(self.dest_dir, "startstr_to_class.json")) as json_file:
            startstr_to_class = json.load(json_file)

        obj_to_class = {}
        for obj in obj_to_colors.keys():
            for startstr in startstr_to_class.keys():
                if obj.startswith(startstr):
                    obj_to_class[obj] = startstr_to_class[startstr]

        with open(self.obj_to_class_file, 'w') as json_file:
            json.dump(obj_to_class, json_file)
