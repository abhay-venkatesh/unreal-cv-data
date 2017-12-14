from __future__ import division, absolute_import, print_function
import os, sys, time, re, json
import numpy as np
import random
import matplotlib.pyplot as plt
from PIL import Image
import StringIO
import json
import cv2

imread = plt.imread
def imread8(im_file):
    ''' Read image as a 8-bit numpy array '''
    im = np.asarray(Image.open(im_file))
    return im

def read_png(res):
    img = Image.open(StringIO.StringIO(res))
    return np.array(img)

def read_npy(res):
    return np.load(res)

# Matches a color from the object_mask and then returns that region color
def match_color(object_mask, target_color, tolerance=3):
    match_region = np.ones(object_mask.shape[0:2], dtype=bool)
    for c in range(3): # r,g,b
        min_val = target_color[c] - tolerance
        max_val = target_color[c] + tolerance
        channel_region = (object_mask[:,:,c] >= min_val) & (object_mask[:,:,c] <= max_val)
        match_region &= channel_region

    if match_region.sum() != 0:
        return match_region
    else:
        return None
    
# Swap colors method
def swap_color(imgarray, source, dest):
    matched_color = match_color(imgarray, [source.R, source.G, source.B])
    imgarray[:,:,:3][matched_color] = [dest.R, dest.G, dest.B]
    return np.array(imgarray)

"""
Connect to the game
===================
Load unrealcv python client, do :code:`pip install unrealcv` first.

"""

from unrealcv import client
client.connect()
if not client.isconnected():
    print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
    sys.exit(-1)

# Make sure the connection works well

res = client.request('vget /unrealcv/status')
# The image resolution and port is configured in the config file.
print(res)

"""
Get objects
======================
Write a json file with the object and their corresponding classes.

"""

scene_objects = client.request('vget /objects').split(' ')
print('Number of objects in this scene:', len(scene_objects))

if '257' in scene_objects:
    scene_objects.remove('257')

obj_id_to_class = {}
for obj_id in scene_objects:
    obj_id_parts = obj_id.split('_')
    class_name = obj_id_parts[0]    
    obj_id_to_class[obj_id] = class_name

# Write JSON file
with open('../data/neighborhood_object_ids.json', 'w') as outfile:
    json.dump(obj_id_to_class, outfile)

"""
Get object colors
======================
First we create the color object class

"""

class Color(object):
    ''' A utility class to parse color value '''
    regexp = re.compile('\(R=(.*),G=(.*),B=(.*),A=(.*)\)')
    def __init__(self, color_str):
        self.color_str = color_str
        match = self.regexp.match(color_str)
        (self.R, self.G, self.B, self.A) = [int(match.group(i)) for i in range(1,5)]

    def __repr__(self):
        return self.color_str

# Then, we load from json
id2color = {}
with open('../data/id2color.json') as data_file:
    data = json.load(data_file)

for obj_id in data.keys():
    color_map = data[obj_id]
    color_str = '(R=' + str(color_map['R']) + ',G=' + \
                str(color_map['G']) + ',B=' + str(color_map['B']) + \
                ',A=' + str(color_map['A']) + ')'
    color = Color(color_str)
    id2color[obj_id] = color

# Map classes to lists of objects
classes = {}

for obj_id in obj_id_to_class.keys():
    
    curr_class = obj_id_to_class[obj_id]
    if curr_class not in classes:
        classes[curr_class] = []
    
    classes[curr_class].append(obj_id)

# Write classes to json
with open('../data/neighborhood_classes.json', 'w') as outfile:
    json.dump(classes, outfile) 
    
# Normalize using built in API
counter = 0
for curr_class in classes.keys():
    
    
    object_list = classes[curr_class]
    curr_color = id2color[object_list[0]]
    
    for obj_id in object_list:
        
        client.request('vset /object/' + obj_id + '/color ' + \
                       str(curr_color.R) + ' ' + str(curr_color.G) + \
                       ' ' + str(curr_color.B))
        
        print(str(counter) + '. vset /object/' + obj_id + '/color ' + \
                       str(curr_color.R) + ' ' + str(curr_color.G) + \
                       ' ' + str(curr_color.B))
    
        counter += 1

"""
Begin Data Collection (Without Normalization)
======
"""
with open('../data/finalTopClassesToColor.json', 'r') as infile:
    top20tocolor = json.load(infile)

top20toint = {}
for cnt, cls in enumerate(top20tocolor.keys()):
    top20toint[cls] = cnt + 1

top20toint['Oak'] = top20toint['Fir']
top20toint['Birch'] = top20toint['Fir']
top20toint['Tree'] = top20toint['Fir']

with open('../data/topClassesToInt.json', 'w') as outfile:
    json.dump(top20toint, outfile)

for batch in range(1,1001):

    # Get random location
    z = 300
    x = random.randint(-5500, 5500)
    y = random.randint(-5500, 5500)
    
    # Get random yaw
    yaw = random.randint(0,360)

    # Coordinates x, y, z
    client.request('vset /camera/0/location ' + str(x) + ' ' + str(y) + \
                   ' ' + str(z)) 

    # Get 10 shots in a series
    angles = []
    a = 0
    while len(angles) < 20:
        angles.append(a)
        a -= 3

    # Increment height sequentially
    heights = []
    height = 300
    while len(heights) < 20:
        heights.append(height)
        height += 50

    for i,angle in enumerate(angles):
        
        print("Round: " + str(batch) + " , Image: " + str(i))
        
        # x, y, z
        client.request('vset /camera/0/location ' + str(x) + ' ' + str(y) + \
                       ' ' + str(heights[i])) 

        # Pitch, yaw, roll
        client.request('vset /camera/0/rotation ' + str(angle) + ' ' + str(yaw) + ' 0')

        # Get Ground Truth
        res = client.request('vget /camera/0/object_mask png')
        object_mask = read_png(res)
        segmentation_image = Image.fromarray(object_mask)
        
        directory = 'D:/dataset_randomyaw/batch11/round' + str(batch) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
                    
        segmentation_image.save('D:/dataset_randomyaw/batch11/round' + str(batch) + '/seg' + \
                            str(i) + '.png')
        
        print('D:/dataset_randomyaw/batch11/round' + str(batch) + '/seg' + \
                            str(i) + '.png')
        
        res = client.request('vget /camera/0/lit png')
        normal = read_png(res)
        normal = Image.fromarray(normal)
        
       
        normal.save('D:/dataset_randomyaw/batch11/round' + str(batch) + '/pic' + \
                            str(i) + '.png')
    
        
        print("Images written. ")