from lib.misc import Color, colors_match
from pathlib import Path
from tqdm import tqdm
from unrealcv import client
import csv
import json
import os


class PreProcessor:
    def __init__(self, dest_dir):
        self.dest_dir = Path(dest_dir, "info")
        self.obj_to_color_file = Path(self.dest_dir, "obj_to_color.json")
        self.obj_to_class_file = Path(self.dest_dir, "obj_to_class.json")
        self.class_to_color_file = Path(self.dest_dir, "class_to_color.json")
        if not os.path.exists(self.obj_to_color_file):
            self._build_obj_to_color()
        else:
            with open(self.obj_to_color_file) as json_file:
                self.obj_to_color = json.load(json_file)

        if not os.path.exists(self.obj_to_class_file):
            self._build_obj_to_class()
        else:
            with open(self.obj_to_class_file) as json_file:
                self.obj_to_class = json.load(json_file)

        if not os.path.exists(self.class_to_color_file):
            self._build_class_to_color()
        else:
            with open(self.class_to_color_file) as json_file:
                self.class_to_color = json.load(json_file)

    def preprocess(self):
        self._set_env_colors()

    def get_obj_from_color(self, color):
        for obj, color_ in self.obj_to_color.items():
            color_ = Color(color_)
            if colors_match(color, color_):
                return obj

    def condense_colors(self):
        condensed_obj_to_color = {}
        for obj, color in self.obj_to_color.items():
            if obj in self.obj_to_class.keys():
                condensed_obj_to_color[self.obj_to_class[obj]] = color
            else:
                condensed_obj_to_color[obj] = color

        with open(Path(self.dest_dir, "condensed_obj_to_color.json"),
                  'w') as json_file:
            json.dump(condensed_obj_to_color, json_file)

    def _set_env_colors(self):
        print("Setting colors...")
        for obj in tqdm(self.obj_to_color.keys()):
            if obj in self.obj_to_class.keys():
                class_ = self.obj_to_class[obj]
                color = Color(self.class_to_color[class_])
                request_str = (
                    "vset /object/" + obj + "/color {r} {g} {b}").format(
                        r=color.R, g=color.G, b=color.B)
            else:
                request_str = (
                    "vset /object/" + obj + "/color {r} {g} {b}").format(
                        r=0, g=0, b=0)
            client.request(request_str)

    def _build_obj_to_color(self):
        scene_objects = client.request('vget /objects').split(' ')
        print('Number of objects in this scene:', len(scene_objects))

        colors = {}
        for scene_obj in tqdm(scene_objects):
            request_str = "vget /object/" + scene_obj + "/color"
            colors[scene_obj] = client.request(request_str)
        with open(self.colors_file, 'w') as fp:
            json.dump(colors, fp)

    def _build_obj_to_class(self):
        with open(self.obj_to_color_file) as json_file:
            obj_to_color = json.load(json_file)

        with open(Path(self.dest_dir, "startstr_to_class.json")) as json_file:
            startstr_to_class = json.load(json_file)

        obj_to_class = {}
        for obj in obj_to_color.keys():
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