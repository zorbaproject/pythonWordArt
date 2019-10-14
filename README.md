# pythonWordArt

Make WordArt, like the ones in MS Office, using Python3.
The actual WordArt generation is performed by a forked version of CSS3 WordArt by Arizzitano: https://github.com/arizzitano/css3wordart
This Python class is just producing the correct HTML code, converting it into PDF, and then into a PNG image. Basically, the HTML get rendered by a QWebEnginePage and printed in PDF. Then, the PDF gets rasterized into a PNG, trying to calculate the correct size of the final image.

## Requirements: 
PySide2: https://pypi.org/project/PySide2/
Python Poppler Qt5: https://pypi.org/project/python-poppler-qt5/

