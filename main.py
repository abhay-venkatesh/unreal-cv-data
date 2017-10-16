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

	# Set to object mask mode
	client.request('vset /viewmode object_mask')

	for batch in range(1,5):

		# Get random location
		z = 300
		x = random.randint(-5000, 5000)
		y = random.randint(-5000, 5000)

		# Coordinates x, y, z
		client.request('vset /camera/0/location ' + str(x) + ' ' + str(y) + ' ' + str(z)) 

		# Get 10 shots in a series
		angles = []
		a = 0
		while len(angles) < 10:
			angles.append(a)
			a -= 6

		# Increment height sequentially
		heights = []
		height = 300
		while len(heights) < 10:
			heights.append(height)
			height += 100

		for i,angle in enumerate(angles):

			# x, y, z
			client.request('vset /camera/0/location ' + str(x) + ' ' + str(y) + ' ' + str(heights[i])) 

			# Pitch, yaw, roll
			client.request('vset /camera/0/rotation ' + str(angle) + ' 0 0')

		  	res = client.request('vget /camera/0/lit ./batch' + str(batch) + '/lit' + str(i) + '.png')
			print('The image is saved to %s' % res)