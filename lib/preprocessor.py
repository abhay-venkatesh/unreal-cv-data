from pathlib import Path
from tqdm import tqdm
from unrealcv import client
import json
import os
import re
import csv


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
        self.obj_to_color_file = Path(self.dest_dir, "obj_to_color.json")
        self.obj_to_class_file = Path(self.dest_dir, "obj_to_class.json")
        self.class_to_color_file = Path(self.dest_dir, "class_to_color.json")

    def preprocess(self):
        if not os.path.exists(self.obj_to_color_file):
            self._build_obj_to_color()
        if not os.path.exists(self.obj_to_class_file):
            self._build_obj_to_class()
        if not os.path.exists(self.class_to_color_file):
            self._build_class_to_color()

    def _build_obj_to_color(self):
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
        with open(self.obj_to_color_file) as json_file:
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

    def _build_class_to_color(self):
        with open(self.obj_to_color_file) as json_file:
            obj_to_colors = json.load(json_file)

        with open(self.obj_to_class_file) as json_file:
            obj_to_class = json.load(json_file)

        class_to_color = {}
        if os.path.exists(Path(self.dest_dir, "target_class_to_color.csv")):
            with open(Path(self.dest_dir,
                           "target_class_to_color.csv")) as csv_file:
                reader = csv.reader(csv_file, delimiter=",")
                for row in reader:
                    class_ = row[0]
                    r, g, b = row[1], row[2], row[3]
                    color = "(R={r},G={g},B={b},A=255)".format(r=r, g=g, b=b)
                    class_to_color[class_] = color
        else:
            for obj in obj_to_class.keys():
                class_ = obj_to_class[obj]
                if class_ not in class_to_color.keys():
                    class_to_color[class_] = obj_to_colors[obj]

        with open(self.class_to_color_file, 'w') as json_file:
            json.dump(class_to_color, json_file)