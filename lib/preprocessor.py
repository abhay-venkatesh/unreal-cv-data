from pathlib import Path
from tqdm import tqdm
from unrealcv import client
import json
import os
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
        self.dest_dir = Path(dest_dir, "json")
        self.colors_file = Path(self.dest_dir, "colors.json")

    def preprocess(self):
        if not os.path.exists(self.colors_file):
            self._get_colors()
        self._condense_colors()

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

    def _condense_colors(self):
        with open(self.colors_file) as fp:
            colors = json.load(fp)
        condensed_colors = {}
        scene_obj_to_class = {}
        for scene_obj, rgba in colors.items():
            first_item = scene_obj.split("_")[0]
            if first_item == "Road" or first_item == "Hedge":
                if first_item not in condensed_colors.keys():
                    condensed_colors[first_item] = rgba
                scene_obj_to_class[scene_obj] = first_item
            else:
                condensed_colors[scene_obj] = rgba

        with open(Path(self.dest_dir, "condensed_colors.json"), 'w') as fp:
            json.dump(condensed_colors, fp)
        with open(Path(self.dest_dir, "scene_obj_to_class.json"), 'w') as fp:
            json.dump(scene_obj_to_class, fp)
