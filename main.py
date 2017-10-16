from __future__ import division, absolute_import, print_function
import os, sys, time, re, json
import numpy as np
import matplotlib.pyplot as plt
import random
from unrealcv import client

client.connect()
if not client.isconnected():
    print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
    sys.exit(-1)
else:

	for batch in range(1,1001):

		# Get random location
		z = 300
		x = random.randint(-5000, 5000)
		y = random.randint(-5000, 5000)

		# Coordinates x, y, z
		client.request('vset /camera/0/location ' + str(x) + ' ' + str(y) + ' ' + str(z)) 

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

			# x, y, z
			client.request('vset /camera/0/location ' + str(x) + ' ' + str(y) + ' ' + str(heights[i])) 

			# Pitch, yaw, roll
			client.request('vset /camera/0/rotation ' + str(angle) + ' 0 0')

		  	res = client.request('vget /camera/0/object_mask ./batch/round' + str(batch) + '/lit' + str(i) + '.png')
			print('The image is saved to %s' % res)