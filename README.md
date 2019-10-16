# pythonWordArt

Make WordArt, like the ones in MS Office, using Python3. \
The actual WordArt generation is performed by a forked version of CSS3 WordArt by Arizzitano: https://github.com/arizzitano/css3wordart
This Python class is just producing the correct HTML code, converting it into PDF, and then into a PNG image. Basically, the HTML get rendered by a QWebEnginePage and printed in PDF. Then, the PDF gets rasterized into a PNG, trying to calculate the correct size of the final image.

## Requirements 
* PySide2: https://pypi.org/project/PySide2/
* Python Poppler Qt5: https://pypi.org/project/python-poppler-qt5/ 

If you install pythonWordArt with pip
```
pip install pythonWordArt
```
all the requirements will be installed automatically.

## Example

This is a minimalistic example:
```
from pythonWordArt import pyWordArt
w = pyWordArt()
w.render3D = True
fileName = "temp"
w.WordArt("Text here", w.Styles["rainbow"], "100", fileName)
```
The first argument is the text, the second is the Style (which needs to be choosen from the **Styles** list) and the third is the size of the font used to write the WordArt. The fourth argument is the filename, without extension, for output. \
If you specify render3D, the library will attempt to draw the 3D effects. If you don't specify this flag, the rendering will be faster and more reliable, but will not have 3D effects. \
To try out all the styles, you can run a demo:
```
from pythonWordArt import pyWordArt
w = pyWordArt()
tmpdirname = ""
with tempfile.TemporaryDirectory() as dirname:
tmpdirname = dirname
os.mkdir(tmpdirname)
print(tmpdirname)
w.canvasWidth = 1754
w.canvasHeight = 1240
w.render3D = True
w.demo(tmpdirname, "100")
```
It's a good idea to set the canvas size, in particular if you are writing a long text. If you need to get the background transparent, you can set
```
w.transparentBackground = True
```
before calling the function **WordArt** or **demo**.

## Thanks to
Arizzitano for his WordArt in CSS3+Javascript: https://github.com/arizzitano/css3wordart
