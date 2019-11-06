#!/usr/bin/python3

#Python WordArt creator
#by Luca Tringali
#Create images with MS Office WordArt styles, using Python

#The original "engine" is:
#CSS3 WordArt by Arizzitano: https://github.com/arizzitano/css3wordart
#This Python class is just producing the correct HTML code, converting it into PDF, and then into a PNG image

#Requirements: 
#PySide2: https://pypi.org/project/PySide2/


import sys
import os
import os.path
import time
import tempfile
from subprocess import Popen, PIPE
import io
import base64

from PySide2.QtWidgets import QApplication, QLabel
from PySide2 import QtCore, QtGui, QtNetwork, QtWebEngineWidgets, QtWidgets


class pyWordArt:
    def __init__(self, text = "WordArt Test", style = 15,  size = 100, noOpenGL = False):
        
        self.Styles = {'outline' : 0, 'up' : 1, 'arc' : 2, 'squeeze' : 3, 'inverted-arc' : 4, 'basic-stack' : 5, 'italic-outline' : 6, 'slate' : 7, 'mauve' : 8, 'graydient' : 9, 'red-blue' : 10, 'brown-stack' : 11, 'radial' : 12, 'purple' : 13, 'green-marble' : 14, 'rainbow' : 15, 'aqua' : 16,'texture-stack' : 17, 'paper-bag' : 18, 'sunset' : 19, 'tilt' : 20, 'blues' : 21, 'yellow-dash' : 22, 'green-stack' : 23, 'chrome' : 24, 'marble-slab' : 25, 'gray-block' : 26, 'superhero' : 27, 'horizon' : 28, 'stack-3d' : 29}
        
        self.noOpenGL = noOpenGL
        #better safe than sorry
        if self.noOpenGL==False and sys.platform != "win32" and sys.platform != "darwin":
            if not self.__X_is_running():
                self.noOpenGL = True
        
        arglist = [sys.argv[0], "--disable-web-security"]
        if self.noOpenGL:
            arglist.append("-platform")
            arglist.append("minimal")
        
        self.__app = QApplication(arglist)
        
        #Required properties:
        self.text = text
        self.size = size
        self.style = style
        #Optional properties:
        self.transparentBackground = False
        self.canvasWidth = 1754 #3508
        self.canvasHeight = 1240 #2480
        
        
    def WordArt(self, wordartText, wordartStyle, wordartSize):
        self.text = wordartText
        self.style = wordartStyle
        self.size = wordartSize

    
    def toHTML(self, wordartText, wordartStyle, wordartSize):
        srcfolder = os.path.abspath(os.path.dirname(__file__))
        myhtml = "<!DOCTYPE html>"
        myhtml = myhtml + "<html>"
        myhtml = myhtml + "<head>"
        myhtml = myhtml + "<title>CSS3 WordArt</title>"
        myhtml = myhtml + "<link href=\"file://"+srcfolder+"/css3wordart/css/style.css\" rel=\"stylesheet\" type=\"text/css\" />"
        myhtml = myhtml + "<script src=\"file://"+srcfolder+"/css3wordart/js/object-observe-lite.js\"></script>"
        myhtml = myhtml + "<script src=\"file://"+srcfolder+"/css3wordart/js/wordart.js\"></script>"
        myhtml = myhtml + "</head>"
        myhtml = myhtml + "<body>"
        myhtml = myhtml + "<input type=\"hidden\" id=\"canvasWidth\" name=\"canvasWidth\" value=\""+ str(self.canvasWidth)+"\">"
        myhtml = myhtml + "<input type=\"hidden\" id=\"canvasHeight\" name=\"canvasHeight\" value=\""+str(self.canvasHeight)+"\">"
        myhtml = myhtml + "<input type=\"hidden\" id=\"wordart-style\" name=\"wordart-style\" value=\""+str(wordartStyle)+"\">"
        myhtml = myhtml + "<input type=\"hidden\" id=\"wordart-size\" name=\"wordart-size\" value=\""+str(wordartSize)+"\">"
        myhtml = myhtml + "<section class=\"background\">"
        myhtml = myhtml + "<template id=\"bgWordart\">"
        myhtml = myhtml + "<div class=\"wordart\">"
        myhtml = myhtml + "<center><span class=\"text\" id=\"wordart-text\" name=\"wordart-text\" data-text=\""+wordartText+"\">"+wordartText+"</span></center>"
        myhtml = myhtml + "</div>"
        myhtml = myhtml + "</template>"
        myhtml = myhtml + "</section>"
        myhtml = myhtml + "</body>"
        myhtml = myhtml + "</html>"
        return myhtml

    
    def toFile(self, filename):
        self.imgName = filename
        if not bool(self.imgName.endswith(".png") or self.imgName.endswith(".jpg") or self.imgName.endswith(".jpeg") or self.imgName.endswith(".gif") or self.imgName.endswith(".tif") or self.imgName.endswith(".tiff") or self.imgName.endswith(".bmp")):
            self.imgName = self.imgName + ".png"
        
        self.__render()

        return self.imgName
    
    def toBase64(self):
        self.__buffer = QtCore.QBuffer()
        self.__buffer.open(QtCore.QBuffer.ReadWrite)
        
        self.__render()

        b64 = self.__buffer.data().toBase64().data()
        return b64
    
        
    def toBufferIO(self):
        b64 = self.toBase64()
        return io.BytesIO(base64.decodebytes(b64))

    
    def __render(self):
        self.__view = QtWebEngineWidgets.QWebEngineView()
        self.__view.setFixedSize(self.canvasWidth,self.canvasHeight)
        self.__view.loadFinished.connect(self.__grabimage)

        myhtml = self.toHTML(self.text, self.style, self.size)
        
        self.__view.setHtml(myhtml)
        self.__view.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
        self.__view.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.__view.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.__view.setAttribute(QtCore.Qt.WA_AlwaysStackOnTop, True)
        self.__view.show()
        
        self.__app.exec_()
        
    
    def __grabimage(self):
        pixmap = self.__view.grab()
        image = self.__cropImage(pixmap.toImage(), self.transparentBackground)
        useBuffer = True
        try:
            if not self.__buffer.isOpen():
                useBuffer = False
        except:
            useBuffer = False
        if useBuffer:
            image.save(self.__buffer, "PNG")
            time.sleep(0.1) 
            self.__buffer.close()
        else:
            image.save(self.imgName)
            while not os.path.isfile(self.imgName):
                time.sleep(0.1)
            time.sleep(0.1)   #sometimes we need a little bit more just to be sure the file has actually been written
        self.__view.hide()
        self.__app.exit()
    
    
    def __cropImage(self, origimage, transparentBackground = False):
        maxX = 0
        minX = origimage.width()
        maxY = 0
        minY = origimage.height()
        exclusionColor = QtGui.QColor(255, 255, 255, 255)

        for x in range(origimage.width()):
            for y in range(origimage.height()):
                if QtGui.QColor.fromRgb(origimage.pixel(x, y)) != exclusionColor:
                    if x < minX:
                        minX = x
                    if x > maxX:
                        maxX = x
                    if y < minY:
                        minY = y
                    if y > maxY: 
                        maxY = y

        if minX > maxX or minY > maxY:
            myimage = origimage
        else:
            myimage = origimage.copy(minX, minY, maxX-minX, maxY-minY)
            
        if transparentBackground:
            newimage = QtGui.QImage(myimage.width(),myimage.height(),QtGui.QImage.Format_ARGB32)
            for x in range(myimage.width()):
                for y in range(myimage.height()):
                    tmpcolor = QtGui.QColor.fromRgb(myimage.pixel(x, y))
                    if tmpcolor == exclusionColor:
                        newimage.setPixelColor(x,y,QtGui.QColor(0, 0, 0, 0))
                    else:
                        newimage.setPixelColor(x,y,tmpcolor)
            myimage = newimage
        return myimage
    
    
    def __X_is_running(self):
        try:
            #thanks to : https://stackoverflow.com/questions/1027894/detect-if-x11-is-available-python, it's much more clean than my original idea
            p = Popen(["xset", "-q"], stdout=PIPE, stderr=PIPE)
            p.communicate()
            return p.returncode == 0
        except:
            return False

        
    def demo(self, dirName, wordartSize = 100):
        if not os.path.isdir(dirName):
            print("Not a folder")
            return
        for elem in self.Styles:
            self.WordArt("WordArt Test", self.Styles[elem], wordartSize)
            self.toFile(dirName + "/demo-" + elem + ".png")



if __name__ == "__main__":
    w = pyWordArt()
    tmpdirname = ""
    with tempfile.TemporaryDirectory() as dirname:
        tmpdirname = dirname
    os.mkdir(tmpdirname)
    print(tmpdirname)
    w.canvasWidth = 1754
    w.canvasHeight = 1240
    #w.transparentBackground = True
    w.demo(tmpdirname, "100")
