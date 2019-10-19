#!/usr/bin/python3
import sys
import os.path
from pythonWordArt import pyWordArt

fileName = "temp2"
if len(sys.argv) >1:
    if os.path.isdir(os.path.abspath(os.path.dirname(sys.argv[1]))) and not os.path.isfile(os.path.abspath(sys.argv[1])):
        fileName = sys.argv[1]
print(fileName)

w = pyWordArt()
w.WordArt("Text here", w.Styles["rainbow"], "100", fileName)
