"""
Resizes dataset

1. Converts PNGs to JPEGs
2. Renames them appropriately with angles attached
"""
from PIL import Image
import os

# Build output directories
output_directory = "../../../../UnrealEngineSourceResized/"
if not os.path.exists(output_directory):
  os.makedirs(output_directory) 

source_directory = "../../../../UnrealEngineSource/"

# Walk through the DatasetSource and pick samples
for dirName, subdirList, fileList in os.walk(source_directory):
  absDirName = os.path.abspath(dirName)
  newDirName = absDirName.replace("UnrealEngineSource", "UnrealEngineSourceResized")
  if not os.path.exists(newDirName):
    os.makedirs(newDirName) 

  for fname in fileList:
    print(dirName + '\\' + fname)
    im = Image.open(dirName + '\\' + fname)
    im = im.convert('RGB')
    im.save(newDirName + '\\' + fname.replace('png', 'jpg'), 'JPEG', quality=90)
