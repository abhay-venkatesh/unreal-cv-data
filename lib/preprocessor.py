from unrealcv import client
from tqdm import tqdm
import json


class PreProcessor:
    def __init__(self):
        pass

    def preprocess(self):
        self._get_colors()

    def _get_colors():
        client.connect()
        if not client.isconnected():
            raise RuntimeError("Could not connect to client. ")

        scene_objects = client.request('vget /objects').split(' ')
        print('Number of objects in this scene:', len(scene_objects))

        colors = dict()
        for scene_obj in tqdm(scene_objects):
            color = client.request("vget /object/" + scene_objects[0] +
                                   "/color")
            if color != "(R=0,G=0,B=0,A=255)":
                print(scene_obj, color)
                colors[scene_obj] = color
            if len(colors) == 10:
                break
        with open('data/colors.json', 'w') as fp:
            json.dump(colors, fp)