# pythonWordArt

Make WordArt, like the ones in MS Office, using Python3. \
The actual WordArt generation is performed by a forked version of CSS3 WordArt by Arizzitano (<https://github.com/arizzitano/css3wordart>), this Python class is just producing the correct HTML code, rendering it into a Qt widget, and then saving into a PNG image. Basically, the HTML get rendered by a QWebEngineView which is not being shown on screen. Then, the widget contents get stored into a PNG image and cropped in order to oly include the actual WordArt. It's also possible to get a transparent background.

## Requirements 
* PySide2: https://pypi.org/project/PySide2/

If you install pythonWordArt with pip
```
pip install pythonWordArt
```
the PySide2 library will be installed automatically. Anyway, if you are installing this on a Linux server, you might need to install also these libraries using your package manager:
```
sudo apt-get install libgl1-mesa-dri libgl1-mesa-glx libnss3 libfontconfig1 libxcomposite1 libxcursor1 libxi6 libxtst6 libasound2
```
you don't need a full Xorg running, just the base libraries. The only problem is that if you don't have a Xorg screen you cannot use the OpenGL effects, so a handful of WordArt styles will not be available. You can check that running the **demo**.

## Simple test

If you run the **main.py** file it will print the name a temporary folder: all the files for the demo will be created in that folder. \
It's also available a test program that you can run without arguments, or with two arguments. For example, if you want to create an image called **example.png** using the style **rainbow** just run this:
```
python3 test.py example.png rainbow
```
if you want to know all styles name, please keep reading.

## Example code

This is a minimalistic example:
```
from pythonWordArt import pyWordArt
w = pyWordArt()
w.WordArt("Text here", w.Styles["rainbow"], 100, "temp.png")
```
The first argument is the text, the second is the Style (which needs to be choosen from the **Styles** list) and the third is the size of the font used to write the WordArt. The fourth argument is the filename, without extension, for output. \
If you specify render3D, the library will attempt to draw the 3D effects. If you don't specify this flag, the rendering will be faster and more reliable, but will not have 3D effects. \
To try out all the styles, you can run a demo:
```
import tempfile
import os
from pythonWordArt import pyWordArt
w = pyWordArt()
# Creating a temporary folder
tmpdirname = ""
with tempfile.TemporaryDirectory() as dirname:
tmpdirname = dirname
os.mkdir(tmpdirname)
print(tmpdirname)
# Set drawing canvas size, optional but recommended
w.canvasWidth = 1754
w.canvasHeight = 1240
# Run the demo
w.demo(tmpdirname, 100)
```
It's a good idea to set the canvas size, in particular if you are writing a long text. A note: running the demo, some images might not be written correctly. This happens because some WordArt need some more time, and if you create too many one after the other the QWebEngineView does not have the time to clear its content. This does not happen if you wait between the creation of two WordArt. \
If you need to get the background transparent, you can set
```
w.transparentBackground = True
```
before calling the function **WordArt** or **demo**.

## Styles

These are all the available styles:
* outline 
* up 
* arc 
* squeeze 
* inverted-arc 
* basic-stack 
* italic-outline 
* slate 
* mauve 
* graydient 
* red-blue 
* brown-stack 
* radial 
* purple 
* green-marble 
* rainbow 
* aqua 
* texture-stack 
* paper-bag 
* sunset 
* tilt 
* blues 
* yellow-dash 
* green-stack 
* chrome 
* marble-slab 
* gray-block 
* superhero 
* horizon 
* stack-3d

You can find all the images in the [examples](https://github.com/zorbaproject/pythonWordArt/tree/master/examples) folder.

## HTML

There is a simple [HTML example](https://rawcdn.githack.com/zorbaproject/pythonWordArt/master/pythonWordArt/example.html) in the pythonWordArt folder, of course you need also the css3wordart subfolder to make it work. To change the text, just look for the **wordart-text** span. The content of the span will become the text, and the the **data-text** property will become the shadow. Usually, text and shadow are the same, but you can always use different phrases.

## Thanks to
Arizzitano for his WordArt in CSS3+Javascript: https://github.com/arizzitano/css3wordart \
The Qt Company for PySide2
