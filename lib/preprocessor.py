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
        with open(self.obj_to_class_file) as json_file:
            obj_to_class = json.load(json_file)

    def _condense_colors(self):
        classes = set()
        with open(self.classes_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                classes.add(row[0])
        with open(self.colors_file) as json_file:
            colors = json.load(json_file)

        condensed_colors = {}
        scene_obj_to_class = {}
        for scene_obj, rgba in colors.items():
            class_name_one = scene_obj.split("_")[0]
            class_name_two = "_".join(scene_obj.split("_")[:2])
            class_name = None
            if class_name_one in classes:
                class_name = class_name_one
            elif class_name_two in classes:
                class_name = class_name_two

            if class_name:
                if class_name not in condensed_colors.keys():
                    condensed_colors[class_name] = rgba
                scene_obj_to_class[scene_obj] = class_name
            else:
                condensed_colors[scene_obj] = rgba

        with open(Path(self.dest_dir, "condensed_colors.json"),
                  'w') as json_file:
            json.dump(condensed_colors, json_file)
        with open(Path(self.dest_dir, "scene_obj_to_class.json"),
                  'w') as json_file:
            json.dump(scene_obj_to_class, json_file)
