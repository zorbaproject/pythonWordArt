#!/usr/bin/python3
import sys
import os.path
from pythonWordArt import pyWordArt

fileName = "temp2"
if len(sys.argv) >1:
    if os.path.isdir(os.path.abspath(os.path.dirname(sys.argv[1]))):
        fileName = sys.argv[1]
print(fileName)

mystyle = "rainbow"
if len(sys.argv) >2:
    mystyle = sys.argv[2]

w = pyWordArt()
w.debug = True
w.WordArt("Text here", w.Styles[mystyle], "100")
w.toFile(fileName)

try:
    from PIL import Image
    pil_im = Image.open(w.toBufferIO())
    pil_im.show()
except:
    print("Unable to show image")
