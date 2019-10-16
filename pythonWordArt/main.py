#!/usr/bin/python3

#Python WordArt creator
#by Luca Tringali
#Create images with MS Office WordArt styles, using Python

#The original "engine" is:
#CSS3 WordArt by Arizzitano: https://github.com/arizzitano/css3wordart
#This Python class is just producing the correct HTML code, converting it into PDF, and then into a PNG image

#Requirements: 
#PySide2: https://pypi.org/project/PySide2/
#Python Poppler Qt5: https://pypi.org/project/python-poppler-qt5/


import sys
import os
import os.path
import time
import tempfile

from PySide2.QtWidgets import QApplication, QLabel
from PySide2 import QtCore, QtGui, QtNetwork, QtWebEngineWidgets, QtWidgets

import popplerqt5


class pyWordArt:
    def __init__(self):
        
        self.Styles = {'outline' : '0', 'up' : '1', 'arc' : '2', 'squeeze' : '3', 'inverted-arc' : '4', 'basic-stack' : '5', 'italic-outline' : '6', 'slate' : '7', 'mauve' : '8', 'graydient' : '9', 'red-blue' : '10', 'brown-stack' : '11', 'radial' : '12', 'purple' : '13', 'green-marble' : '14', 'rainbow' : '15', 'aqua' : '16','texture-stack' : '17', 'paper-bag' : '18', 'sunset' : '19', 'tilt' : '20', 'blues' : '21', 'yellow-dash' : '22', 'green-stack' : '23', 'chrome' : '24', 'marble-slab' : '25', 'gray-block' : '26', 'superhero' : '27', 'horizon' : '28', 'stack-3d' : '29'}
        
        self.render3D = False
        self.transparentBackground = False
        
        self.canvasWidth = 1754 #3508
        self.canvasHeight = 1240 #2480
        
        arglist = [sys.argv[0], "--disable-web-security"]
        self.app = QApplication(arglist)
        
        self.profile = QtWebEngineWidgets.QWebEngineProfile()
        self.profile.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.profile.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.profile.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.AllowRunningInsecureContent, True)
        
        self.page = QtWebEngineWidgets.QWebEnginePage(self.profile)
        self.page.loadFinished.connect(self.__printpdf)
        
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setFixedSize(self.canvasWidth,self.canvasHeight)
        
    #def __del__(self):
        #self.app.exit()

    def __printpdf(self):
        if self.render3D:
            pixmap = self.view.grab()
            self.imgName = self.pdfName.replace(".pdf",".png")
            image = self.cropImage(pixmap.toImage(), self.transparentBackground)
            image.save(self.imgName)
            while not os.path.isfile(self.imgName):
                time.sleep(0.1)
            self.view.hide()
            self.app.exit()
        else:
            self.page.pdfPrintingFinished.connect(self.__doneprinting)
            self.page.printToPdf(self.pdfName, QtGui.QPageLayout(QtGui.QPageSize(QtCore.QSize(self.canvasWidth,self.canvasHeight)), QtGui.QPageLayout.Portrait, QtCore.QMarginsF()))
    
    def __doneprinting(self):
        self.imgName = self.pdfName.replace(".pdf",".png")
        while not bool(os.path.isfile(self.pdfName) or os.path.isfile(self.imgName)):
            time.sleep(0.1)
        try:
            if os.path.isfile(self.pdfName):
                d = popplerqt5.Poppler.Document.load(self.pdfName)
            pdfPage = d.page(0)
        except:
            self.app.exit()
            return
        image = pdfPage.renderToImage(150, 150, -1, -1, -1, -1)
        image = self.cropImage(image, self.transparentBackground)
        image.save(self.imgName)
        while not os.path.isfile(self.imgName):
            time.sleep(0.1)
        if os.path.isfile(self.pdfName):
            os.remove(self.pdfName)
        #print(self.imgName)
        self.app.exit()
        
    def WordArtHTML(self, wordartText, wordartStyle, wordartSize):
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
        myhtml = myhtml + "<input type=\"hidden\" id=\"wordart-style\" name=\"wordart-style\" value=\""+wordartStyle+"\">"
        myhtml = myhtml + "<input type=\"hidden\" id=\"wordart-size\" name=\"wordart-size\" value=\""+wordartSize+"\">"
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
    
    def WordArt(self, wordartText, wordartStyle, wordartSize, filename):
        self.pdfName = filename + ".pdf"
        
        myhtml = self.WordArtHTML(wordartText, wordartStyle, wordartSize)
        self.page.setHtml(myhtml)
        
        if self.render3D:
            self.view.setPage(self.page)
            self.view.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
            self.view.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
            self.view.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.view.setAttribute(QtCore.Qt.WA_AlwaysStackOnTop, True)
            self.view.show()

        self.app.exec_()
        
    def cropImage(self, origimage, transparentBackground = False):
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
        
    def demo(self, dirName, wordartSize):
        if not os.path.isdir(dirName):
            print("Not a folder")
            return
        for elem in self.Styles:
            self.WordArt("WordArt Test", self.Styles[elem], wordartSize, dirName + "/demo-" + elem)

if __name__ == "__main__":
    w = pyWordArt()
    tmpdirname = ""
    with tempfile.TemporaryDirectory() as dirname:
        tmpdirname = dirname
    os.mkdir(tmpdirname)
    print(tmpdirname)
    w.canvasWidth = 1754
    w.canvasHeight = 1240
    #w.render3D = True
    #w.transparentBackground = True
    w.demo(tmpdirname, "100")
    #fileName = os.path.abspath(os.path.dirname(sys.argv[0]))+"/temp"
    #w.WordArt("Text here", w.Styles["rainbow"], "100", fileName)
