from __future__ import division, absolute_import, print_function
import os, sys, time, re, json
import numpy as np
import matplotlib.pyplot as plt
from unrealcv import client

client.connect()
if not client.isconnected():
    print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
    sys.exit(-1)
else:

	for round in range(1,5):

		# Get random location
		z = 300
		x = randint(-5000, 5000)
		y = randint(-5000, 5000)

		# Coordinates x, y, z
		client.request('vset /camera/0/location ' + str(x) + ' ' + str(y) + ' ' + str(z)) 

		# Get 10 shots in a series
		angles = []
		a = 6
		while len(angles) < 10:
			angles.append(a)
			a += 6

		for angle in angles:

			# Pitch, yaw, roll
			client.request('vset /camera/0/rotation ' + angle + 0 0 0')

		  	res = client.request('vget /camera/0/lit ./batch/lit.png')
			print('The image is saved to %s' % res)