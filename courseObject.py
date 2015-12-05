import globalVar
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from parser import *

class courseObject():
    """
    container/manager for sessions
    courseObject(index,parent);
    **does not own session widgets**
    """
    def __init__(self,parent=None,index=-1):
        #QWidget.__init__(self,parent);
        self.parent = parent;
        self.index = index;
        self.itemList = self.getItemList(index);
        info = globalVar.courseInfo[index];
        self.title = info['title'];

        for item in self.itemList:
            w = sessionWidget(parent = self.parent, title = self.title,loc=item['loc']);
            item['widget'] = w;
            item['widget'].show();
        #self.setAttribute(Qt.WA_TransparentForMouseEvents,True);
        #self.show();
    def setFrameColor(self,col):
        for item in self.itemList:
            item['widget'].setFrameColor(col);
    def setBkColor(self,col):
        for item in self.itemList:
            item['widget'].setBkColor(col);
    def clear(self):
        for item in self.itemList:
            item['widget'].deleteLater();
    def getItemList(self,i): # will now return a list of rects
        """
        ##TEXT
        """
        return list(globalVar.courseInfo[i]['meetingPattern']); #mp[] << {day,time[start,end],loc}
    def resize(self,w,h):
        width = w/5;
        ratio = h/(12*60);
        for item in self.itemList:
            t = item['time'];
            left = width * parseDay(item['day']);
            top = (t[0]-9*60) * ratio;
            bottom = (t[1]-9*60)*ratio;
            item['widget'].move(left,top);
            item['widget'].resize(width,bottom-top);

class sessionWidget(QWidget):
    """
    sessionWidget(parent=None,title='N/A',loc='N/A')
    """
    def __init__(self,parent=None,title='N/A',loc='N/A'):
        QWidget.__init__(self,parent);
        uic.loadUi("sessionWidget.ui",self);
        
        globalVar.courseInfo; 
        self.setTitle(title);
        self.setLocation(loc);
        
        self.setAutoFillBackground(True);
        tCol = QColor.fromRgb(66,66,128,32);
        self.setFrameColor(tCol);
    def setTitle(self,title):
        self.title.setText(title);
        self.title.setToolTip(title);
    def setLocation(self,location):
        self.location.setText(location);
        self.location.setToolTip(location);
    def setFrameColor(self,col):
        pal = self.frame.palette();
        pal.setColor(self.frame.foregroundRole(),col);
        self.frame.setPalette(pal);
    def setBkColor(self,col):
        pal = self.palette();
        pal.setColor(self.backgroundRole(),col);
        self.setPalette(pal);
    def setOptions(self,args):
        d = QDialog(self);
        uic.loadUi("options.ui",d);
        d.exec_();
    def resizeEvent(self,event):
        QWidget.resizeEvent(self,event);
        self.frame.resize(self.width(),self.height());
        self.resizeLabel(self.title);
        self.resizeLabel(self.location);
        self.resizeLabel(self.time);
    def resizeLabel(self,label):
        fit = False;
        string = label.text();
        myFont = label.font();
        tmp = QLabel(string,None,label.windowFlags());
        tmp.setFont(myFont);
        tmp.setWordWrap(True);
        tmp.setMaximumWidth(self.width());
        label.setText("");
        while not fit:
            fm = QFontMetrics(myFont);
            bound = fm.boundingRect(0,0, label.width(), label.height(), Qt.AlignLeft|Qt.TextWordWrap, string);
            if (bound.height() <= label.height()):
                fit = True;
            else:
                if myFont.pointSize() < 4:
                    break;
                myFont.setPointSize(myFont.pointSize() - 1);
                tmp.setFont(myFont);
        label.setFont(myFont);
        label.setText(string);  
        #print(myFont.pointSize());
