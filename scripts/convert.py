import json
import cv2
import numpy as np

data = json.load(open('color_map.json','r'))

color_map = {}

for i, obj in enumerate(data):
	color_map[(data[obj]["R"],data[obj]["G"],data[obj]["B"])] = i

img = cv2.imread('round2/seg3.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
[m,n] = img.shape[:2]
res = np.zeros((m,n))

for i in range(m):
	for j in range(n):
		if color_map.has_key(tuple(img[i][j])):
			res[i][j] = color_map[tuple(img[i][j])]

cv2.imwrite('res.png',res)