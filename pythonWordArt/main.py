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
        
        self.showWindow = False
        #self.showWindow = True
        
        arglist = [sys.argv[0], "--disable-web-security"]
        self.app = QApplication(arglist)
        
        self.profile = QtWebEngineWidgets.QWebEngineProfile()
        self.profile.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.profile.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.profile.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.AllowRunningInsecureContent, True)
        
        self.page = QtWebEngineWidgets.QWebEnginePage(self.profile)
        self.page.loadFinished.connect(self.__printpdf)
        
    #def __del__(self):
        #self.app.exit()

    def __printpdf(self):
        self.page.pdfPrintingFinished.connect(self.__doneprinting)
        self.page.printToPdf(self.pdfName, QtGui.QPageLayout(QtGui.QPageSize(QtGui.QPageSize.A4), QtGui.QPageLayout.Landscape, QtCore.QMarginsF()))
        # TODO: check why QWebEnginePage contentSize is not correct
        #self.page.printToPdf(self.pdfName, QtGui.QPageLayout(QtGui.QPageSize(self.page.contentsSize().toSize(),QtGui.QPageSize.Point), QtGui.QPageLayout.Landscape, QtCore.QMarginsF()))
    
    def __doneprinting(self):
        self.imgName = self.pdfName.replace(".pdf",".png")
        while not bool(os.path.isfile(self.pdfName) or os.path.isfile(self.imgName)):
            time.sleep(1)
        try:
            if os.path.isfile(self.pdfName):
                d = popplerqt5.Poppler.Document.load(self.pdfName)
            pdfPage = d.page(0)
        except:
            self.app.exit()
            return
        zoom = 150/72
        if True:
            height = -1
            width = -1
            xmargin = 0
            ymargin = 0
            for elem in pdfPage.textList():
                tw = elem.boundingBox().x() + elem.boundingBox().width()
                th = elem.boundingBox().y() + elem.boundingBox().height()
                xmargin = xmargin + elem.boundingBox().width()
                #ymargin = ymargin + elem.boundingBox().height()
                if th > height:
                    height = th
                if tw > width:
                    width = tw
            try:
                xmargin = (xmargin/(len(pdfPage.textList())))/2
                ymargin = (ymargin/(len(pdfPage.textList())))/2
            except:
                xmargin = 0
                ymargin = 0
            image = pdfPage.renderToImage(72*zoom, 72*zoom, -1, -1, (width+xmargin)*zoom, (height+ymargin)*zoom)
        else:
            image = pdfPage.renderToImage(150, 150, -1, -1, -1, -1)
        image.save(self.imgName)
        while not os.path.isfile(self.imgName):
            time.sleep(1)
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
        
        if self.showWindow:
            self.view = QtWebEngineWidgets.QWebEngineView()
            self.view.setPage(self.page)
            self.view.show()

        self.app.exec_()
        
    def demo(self, dirName, wordartSize):
        if not os.path.isdir(dirName):
            print("Not a folder")
            return
        for elem in self.Styles:
            self.WordArt("WordArt Test", self.Styles[elem], wordartSize, dirName + "/demo-" + elem)

if __name__ == "__main__":
    w = pyWordArt()
    #fileName = os.path.abspath(os.path.dirname(sys.argv[0]))+"/temp"
    #w.WordArt("Text here", w.Styles["rainbow"], "100", fileName)
    tmpdirname = ""
    with tempfile.TemporaryDirectory() as dirname:
        tmpdirname = dirname
    os.mkdir(tmpdirname)
    print(tmpdirname)
    w.demo(tmpdirname, "100")
