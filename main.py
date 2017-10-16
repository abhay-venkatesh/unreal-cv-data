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
		

		client.request('vset /camera/0/location 5 5 300')
		client.request('vset /camera/0/rotation 5 5 5')
	  	res = client.request('vget /camera/0/lit ./batch/lit.png')
		print('The image is saved to %s' % res)