import globalVar
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from parser import *
from copy import deepcopy

class CourseObject():
    """
    container/manager for sessions
    CourseObject(index,parent);
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
            w = SessionWidget(parent = self.parent, title = self.title,loc=item['loc'],time=item['time']);
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
        return deepcopy(globalVar.courseInfo[i]['meetingPattern']);
    def resize(self,w,h):
        width = w/6;
        ratio = h/(13*60); #leaving space for displaying days on top
        for item in self.itemList:
            t = item['time'];
            left = width * (1 + parseDay(item['day'])); #leaving 1 for time display at left
            top = (t[0]-8*60) * ratio; #leaving space for displaying days
            bottom = (t[1]-8*60)*ratio;
            item['widget'].move(left,top);
            item['widget'].resize(width,bottom-top);

class SessionWidget(QWidget):
    """
    SessionWidget(parent=None,title='N/A',loc='N/A')
    """
    def __init__(self,parent=None,title='N/A',loc='N/A',time=[]):
        QWidget.__init__(self,parent);
        uic.loadUi("SessionWidget.ui",self);
        
        globalVar.courseInfo; 
        self.setTitle(title);
        self.setLocation(loc);
        self.setTime(time);
        self.setAutoFillBackground(True);
        tCol = QColor.fromRgb(66,66,128,32);
        self.setFrameColor(tCol);
    def setTitle(self,title):
        self.title.setText(title);
        self.title.setToolTip(title);
    def setLocation(self,location):
        self.location.setText(location);
        self.location.setToolTip(location);
    def setTime(self,time):
        ts = str(int(time[0]/60))+":"+str(time[0]%60).zfill(2);
        te = str(int(time[1]/60))+":"+str(time[1]%60).zfill(2);
        tstr = ts + ' - ' + te;
        self.time.setText(tstr);
        self.time.setToolTip(tstr);
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
        uic.loadUi("Options.ui",d);
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
            if (bound.height() <= label.height() and bound.width() <= label.width()):
                fit = True;
            else:
                if myFont.pointSize() < 4:
                    break;
                myFont.setPointSize(myFont.pointSize() - 1);
                tmp.setFont(myFont);
        
        while fit:
            fm = QFontMetrics(myFont);
            bound = fm.boundingRect(0,0, label.width(), label.height(), Qt.AlignLeft|Qt.TextWordWrap, string);
            if (bound.height() >= label.height() or  bound.width() >= label.width()):
                fit = False;
                myFont.setPointSize(myFont.pointSize() - 1);
                break;
            myFont.setPointSize(myFont.pointSize() + 1);
            tmp.setFont(myFont);

        label.setFont(myFont);
        label.setText(string);  
        #print(myFont.pointSize());
