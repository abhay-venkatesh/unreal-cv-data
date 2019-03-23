"""
TODO: Complete This


NOTE: The paths in this file only work when running from main.py in the root 
    directory of the repo.

"""


from __future__ import division, absolute_import, print_function
import os, sys, time, re, json
import numpy as np
import random
import matplotlib.pyplot as plt
from PIL import Image
import StringIO
import json
import cv2
class DataCollector:

  def __init__(self):
    pass

  def begin_deux(self):
    # Connect to the game
    from unrealcv import client
    client.connect()
    if not client.isconnected():
      print('UnrealCV server is not running. Run the game downloaded ',
          'from http://unrealcv.github.io first.')
      sys.exit(-1)

    # Make sure the connection works well
    res = client.request('vget /unrealcv/status')
    # The image resolution and port is configured in the config file.
    print(res)

    scene_objects = client.request('vget /objects').split(' ')
    print('Number of objects in this scene:', len(scene_objects))

    # Creates a JSON file that maps each objects ID to a class
    # We use this to group stuff together
    obj_id_to_class = {}
    for obj_id in scene_objects:
      obj_id_parts = obj_id.split('_')
      class_name = obj_id_parts[1]    
      obj_id_to_class[obj_id] = class_name

    # Write JSON file
    with open('../data/neighborhood_deux_object_ids.json', 'w') as outfile:
      json.dump(obj_id_to_class, outfile)



  def imread8(self, im_file):
    """ Read image as a 8-bit numpy array """ 
    im = np.asarray(Image.open(im_file))
    return im

  def read_png(self, res):
    img = Image.open(StringIO.StringIO(res))
    return np.array(img)

  def read_npy(self, res):
    return np.load(res)

  def match_color(self, object_mask, target_color, tolerance=3):
    """ Matches a color from the object_mask and 
      then returns that region color """
    match_region = np.ones(object_mask.shape[0:2], dtype=bool)
    for c in range(3): # r,g,b
      min_val = target_color[c] - tolerance
      max_val = target_color[c] + tolerance
      channel_region = ((object_mask[:,:,c] >= min_val) & 
                (object_mask[:,:,c] <= max_val))
      match_region &= channel_region

    if match_region.sum() != 0:
      return match_region
    else:
      return None
    
  def swap_color(self, imgarray, source, dest):
    matched_color = match_color(imgarray, [source.R, source.G, source.B])
    imgarray[:,:,:3][matched_color] = [dest.R, dest.G, dest.B]
    return np.array(imgarray)

