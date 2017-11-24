import json
import cv2
import numpy as np
from ast import literal_eval

def match_color(object_mask, target_color, tolerance=3):
	match_region = np.ones(object_mask.shape[0:2], dtype=bool)
	for c in range(3):
		min_val = target_color[c] - tolerance
		max_val = target_color[c] + tolerance
		channel_region = (object_mask[:,:,c] >= min_val) & (object_mask[:,:,c] <= max_val)
		match_region &= channel_region

		if match_region.sum() != 0:
			return match_region
		else:
			return None

color2class = json.load(open('finalColorsToClasses.json','r'))
class2num = json.load(open('finalClassesToInt.json','r'))

color_map = {}

for color in color2class:
	color_map[literal_eval(color)] = class2num[color2class[color]]

with open('list','r') as f:
	for i,line in enumerate(f):
		itemname = line.strip()
		filename = '../../../segmentation_data/batch1/' + itemname
		img = cv2.imread(filename)
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		[m,n] = img.shape[:2]
		res = np.zeros((m,n))

		print("Working on" + filename)

		for key in color_map:
			match_region=match_color(img,key)
			if not (match_region is None):
				res = (np.multiply(res, ~match_region)) + match_region*color_map[key]

		outfile = 'converted_data/' + str(i) + '.png' 
		print(outfile)
		cv2.imwrite(outfile,res*8)


