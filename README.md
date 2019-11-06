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
w.WordArt("Text here", w.Styles[mystyle], "100")
w.toFile(fileName)
```
The first argument is the text, the second is the Style (which needs to be choosen from the **Styles** list, but it's a number from 0 to 29) and the third is the size of the font used to write the WordArt. Usually, 100 is a good value. This gives you a pyWordArt object, that you can then write to an image file (usually in PNG) using the **toFile** function. \
Alternatively, you can get the image as a Base64 coded text, thanks to the **toBase64** function. \
It's also possibile to obtain an input-output buffer, useful for libraries that need to open buffers like PIL o Telepot. For example, it can be used like this:
```
from PIL import Image
from pythonWordArt import pyWordArt
w = pyWordArt()
w.WordArt("Text here", w.Styles[mystyle], "100")
pil_im = Image.open(w.toBufferIO())
pil_im.show()
```
If you specify the **noOpenGL** as **True**, the library will load with minimal graphic support, without an OpenGL context to render 3D effects. If you don't specify this flag, the rendering will be done with OpenGL if available. \
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

## List of members
Functions:

### init__(self, text = "WordArt Test", style = 15,  size = 100, noOpenGL = False)
This function initialize the pythonWordArt object. It's possible to call the function with no argoments, and set the basic properties in the next lines of code. Or you can already set the properties here, which is useful if you just want to get one single wordart.
Does not return a value.

### WordArt(self, wordartText, wordartStyle, wordartSize)
This function enables you to set new properties for a WordArt. Basically, you can change the text, the style, or the size all in one line. If you prefer, it's also possible to set the properties manually.
Does not return a value.

### toHTML(self, wordartText, wordartStyle, wordartSize)
Returns a string containing html code that works locally displaying the WordArt.

### toBase64()
Returns the wordart image as a printable string text in Base64 encoding.

### toBufferIO()
Returns an Input Output buffer containing the image. This simulates opening a file withotu actually having to write a file on disk.

### toFile(fileName)
Saves the image in a file. The name fileName can be with or without extension. If the extension is missing, PNG format will be used automatically.
Returns full fileName.

### demo(self, dirName, wordartSize = 100)
This function take a folder path, and eventually the WordArt size, as arguments. It then creates as many wordart files (in PNG format) as the available Styles.
Does not return a value.

Properties:

### noOpenGL = bool
By default set to False. If set to True, the WordArt creation will be performed without OpenGL, which means some Styles will not look good but you'll be able to use it even if you are running it headless without a GPU.

### transparentBackground = bool
By default set to False. If set to True, the WordArt background will become transaprent. If wiriting to a file, please remember to use a format that supports transparency, like PNG.

### canvasWidth = int
By default set to 1754, an A4 page width at 150dpi. It is the width in pixels of the canvas where the WordArt will be drawn: you need to set it accordingly to the length of the text you are going to write. In the future, it will be adjusted automatically.

### canvasHeight = int
By default set to 1240, an A4 page height at 150dpi. It is the height in pixels of the canvas where the WordArt will be drawn: you need to set it accordingly to the length of the text you are going to write. In the future, it will be adjusted automatically.

### text = str
This is the text of the WordArt. Just set whatever you want, but take note that shot texts, less than 3 or 4 words, work best.

### style = int
This is the style of the WordArt, by default it's 15, which is the rainbow style. Take a look at the styles list.

### size = int
This is the size of the WordArt, by default it's 100. If you need a bigger image, ust use a bigger number.

### Styles = dict
This dictionary contains all the styles supported by pythonWordArt. It's easyer to remember the styles by their name nstead of the number.


## HTML

There is a simple [HTML example](https://rawcdn.githack.com/zorbaproject/pythonWordArt/master/pythonWordArt/example.html) in the pythonWordArt folder, of course you need also the css3wordart subfolder to make it work. To change the text, just look for the **wordart-text** span. The content of the span will become the text, and the the **data-text** property will become the shadow. Usually, text and shadow are the same, but you can always use different phrases.

## Thanks to
Arizzitano for his WordArt in CSS3+Javascript: https://github.com/arizzitano/css3wordart \
The Qt Company for PySide2
