from __future__ import division, absolute_import, print_function
import os, sys, time, re, json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

imread = plt.imread
def imread8(im_file):
    ''' Read image as a 8-bit numpy array '''
    im = np.asarray(Image.open(im_file))
    return im

def read_png(res):
    img = Image.open(res)
    return np.asarray(img)

def read_npy(res):
    return np.load(res)


from unrealcv import client
client.connect()
if not client.isconnected():
    print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
    sys.exit(-1)


res = client.request('vget /unrealcv/status')
# The image resolution and port is configured in the config file.
print(res)