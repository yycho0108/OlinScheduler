import globalVar
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from parser import *

class courseObject(QWidget):
    """
    container/manager for sessions
    courseObject(index,parent);
    """
    def __init__(self,parent=None,index=-1):
        QWidget.__init__(self,parent);
        self.index = index;
        self.itemList = self.getItemList(index);
        self.sessionList = [];
        info = globalVar.courseInfo[index];
        self.title = info['title'];

        for item in self.itemList:
            w = sessionWidget(parent = self, title = self.title,loc=item['loc'],rect=item['rect']);
            w.show();
            self.sessionList.append(w);
        self.show();
    def setFrameColor(self,col):
        for w in self.sessionList:
            w.setFrameColor(col);
    def clear(self):
        for w in self.sessionList:
            w.deleteLater();
    def getItemList(self,i): # will now return a list of rects
        """
        getItemList(index) --> list << {rect:QRectF,loc:String}
        """
        itemList = [];
        mp = globalVar.courseInfo[i]['meetingPattern']; #mp[] << {day,time[start,end],loc}
        for s in mp: #s = meeting session
            left = 100*parseDay(s['day']);
            t = s['time'];
            top = t[0] - 60*9;
            height = t[1] - t[0];
            width = 100;
            r = QRectF(left,top,width,height);
            itemList.append({'rect':r,'loc':s['loc']});
        return itemList;

class sessionWidget(QWidget):
    """
    sessionWidget(parent,title,loc,width,height,x,y)
    sessionWidget(parent,title,loc,rect:QRectF)
    sessionWidget(parent,title,loc,rect:QRect)
    """
    def __init__(self,parent=None,title='N/A',loc='N/A',rect=None,width=100,height=100,x=0,y=0):
        
        if rect is not None:
            width = rect.width();
            height = rect.height();
            x = rect.left();
            y = rect.top();
        
        QWidget.__init__(self,parent);
        uic.loadUi("sessionWidget.ui",self);
        
        globalVar.courseInfo; 
        self.setTitle(title);
        self.setLocation(loc);
        
        self.setAutoFillBackground(True);
        tCol = QColor.fromRgb(66,66,128,32);
        self.setFrameColor(tCol);
        self.resize(width,height);
        self.move(x,y);
    
    def setTitle(self,title):
        self.title.setText(title);
    def setLocation(self,location):
        self.location.setText(location);
    def setFrameColor(self,col):
        pal = self.palette();
        pal.setColor(self.frame.foregroundRole(),col);
        self.frame.setPalette(pal);
    def setOptions(self,args):
        d = QDialog(self);
        uic.loadUi("options.ui",d);
        d.exec_();
        pass;
    def resizeEvent(self,event):
        QWidget.resizeEvent(self,event);
        self.frame.resize(self.width(),self.height());
        pass;
