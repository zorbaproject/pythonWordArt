#!/usr/bin/python3
import sys
import os.path
from pythonWordArt import pyWordArt

w = pyWordArt()
fileName = os.path.abspath(os.path.dirname(sys.argv[0]))+"/temp"
w.WordArt("Text here", w.Styles["rainbow"], "100", fileName)
