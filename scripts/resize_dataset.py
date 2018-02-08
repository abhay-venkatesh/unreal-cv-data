"""
Resizes dataset

1. Resize to 720x450
2. Converts PNGs to JPEGs
"""

from PIL import Image
im = Image.open("pic0.png")
rgb_im = im.convert('RGB')
rgb_im.save('pic0.jpg', 'JPEG', quality=90)
