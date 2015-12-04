import pickle

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import re
import sys
import getCourseInfo
#from collections inport namedtuple

RECT_TYPE = 3;
TEXT_TYPE = 8;
courseInfo = []; # global variable

def parseTime(time): #convert to numeric min, 24 hr scale
    time = time.strip();
    reg = r"([0]?[0-9]|1[0-2]):([0-5][0-9])(?:\s)?(?i)(am|pm)"; #regex for time
    
    p = re.compile(reg);
    m = p.search(time);
    
    hr = int(m.group(1));
    mn = int(m.group(2));
    xm = m.group(3);
    
    if hr != 12 and xm.startswith(('p','P')):
        hr += 12;
    elif hr == 12 and xm.startswith(('a','A')):
        hr = 0;
    return hr*60 + mn;
def parseDay(d):
    return 'MTWRF'.find(d);
def parseMeet(inList):
    """
    parseMeet(inList) --> list of {day:String,time[start,end]:list[int,int],loc:String}
    """
    outList = []
    for meet in inList:
        try:
            time,loc = meet.split(';');
            days,time = time.split(' ',1);
            start,end = time.split(' - ',1);
            if start.find('AM') == -1 and start.find('PM') == -1:
                if end.find('AM') != -1:
                    start += ' AM';
                else:
                    start += ' PM';
            for d in days:
                outList.append({
                    'day':d,
                    'time':[parseTime(start),parseTime(end)],
                    'loc':loc
                    });
        except ValueError: #Invalid/Undetermined Meeting Pattern
            pass;
    return outList;
class course(QWidget):
    """
    container/manager for sessions
    course(index,parent);
    """
    def __init__(self,parent=None,index=-1):
        QWidget.__init__(self,parent);
        self.itemList = self.getItemList(index);
        self.sessionList = [];
        info = courseInfo[index];
        self.title = info['title'];

        for item in self.itemList:
            w = sessionWidget(parent = self, title = self.title,loc=item['loc'],rect=item['rect']);
            w.show();
            self.sessionList.append(w);
        self.show();
    def setBkColor(self,col):
        for w in self.sessionList:
            w.setBkColor(col);
    def clear(self):
        for w in self.sessionList:
            w.deleteLater();
    def getItemList(self,i): # will now return a list of rects
        """
        getItemList(index) --> list << {rect:QRectF,loc:String}
        """
        itemList = [];
        mp = courseInfo[i]['meetingPattern']; #mp[] << {day,time[start,end],loc}
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
        
        global courseInfo; 
        self.setTitle(title);
        self.setLocation(loc);
        
        self.setAutoFillBackground(True);
        tCol = QColor.fromRgb(66,66,128,32);
        self.setBkColor(tCol);
        self.optionsBtn.clicked.connect(self.setOptions);
        self.resize(width,height);
        self.move(x,y);
    
    def setTitle(self,title):
        self.title.setText(title);
    def setLocation(self,location):
        self.location.setText(location);
    def setBkColor(self,col):
        pal = self.palette();
        pal.setColor(self.backgroundRole(),col);
        self.setPalette(pal);
    def setOptions(self,args):
        d = QDialog(self);
        uic.loadUi("options.ui",d);
        d.exec_();
        pass;
    def resizeEvent(self,event):
        QWidget.resizeEvent(self,event);
        self.frame.resize(self.width(),self.height());
        pass;
class scheduleView(QGraphicsView):
    def __init__(self, scene,mainWindow):
        self.mainWindow = mainWindow;
        QGraphicsView.__init__(self,scene);
        self.myScene = scene;
        self.resize(500,800);
        self.saveBtn = QPushButton(self);
        self.saveBtn.setText('save');
        self.saveBtn.clicked.connect(self.save);
        self.setWindowTitle('schedule');
        self.prevCourse = None;
        self.courseList = [];
    def closeEvent(self,event):
        self.mainWindow.clear();
        super(scheduleView,self).closeEvent(event);
    def updateDisplay(self):
        #example placeholder code
        print('here');
    def clear(self):
        self.myScene.clear();
    def save(self):
        QPixmap.grabWidget(self).save('schedule.png');
    def getItemList(self,i): # will now return a list of rects
        """
        getItemList(index) --> list << {rect:QRectF,loc:String}
        """
        itemList = [];
        mp = courseInfo[i]['meetingPattern']; #mp[] << {day,time[start,end],loc}
        for s in mp: #s = meeting session
            left = 100*parseDay(s['day']);
            t = s['time'];
            top = t[0] - 60*9;
            height = t[1] - t[0];
            width = 100;
            r = QRectF(left,top,width,height);
            itemList.append({'rect':r,'loc':s['loc']});
        return itemList;
    def preview(self,i):
        if self.prevCourse is not None:
            self.prevCourse.clear();
        self.prevCourse = course(parent=self,index=i);
    def addCourse(self,i):
        cCol = QColor.fromRgb(0,0,0,255);
        self.prevCourse.setBkColor(cCol);
        self.courseList.append(self.prevCourse);
        self.prevCourse = None;
    def removeCourse(self,i):
        pass;
    def paintEvent(self,event):
        QGraphicsView.paintEvent(self,event);
        q = QPainter(self.viewport());

class OS_GUI(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent);
        uic.loadUi('mainwindow.ui',self);
        self.pool.activated.connect(self.onSelectClass);
        self.loadData();
        self.onOpenSchedule();
        self.addBtn.clicked.connect(self.addCourse);
        self.removeBtn.clicked.connect(self.removeCourse);
        self.clearBtn.clicked.connect(self.clear);
        self.openSchedule.clicked.connect(self.onOpenSchedule);
        self.actionTitle.triggered.connect(self.visual.updateDisplay);

    def loadData(self):
        with open('courseInfo.dat', 'rb') as f_in:
            self.pool.blockSignals(True);
            self.pool.clear();
            global courseInfo;
            courseInfo = pickle.load(f_in);
            for course in courseInfo:
                # make numeric
                course['meetingPattern'] = parseMeet(course['meetingPattern']);
                self.pool.addItem(course['title']);
            self.pool.blockSignals(False);

    def onOpenSchedule(self):
        self.visual = scheduleView(QGraphicsScene(self),self); #beware: not a parent
        self.visual.show();
    def onSelectClass(self, index):
        global courseInfo; 
        info = courseInfo[index];
        self.code.setText(info['code']);
        self.title.setText(info['title']);
        self.instructors.clear();
        self.instructors.addItems(info['instructor']);
        self.credit.setText(info['credit']);
        #self.myCourses.model().insertRow(3);
        #qm.setData(qm.rowCount(), info['code'] + ' : ' + info['title']);
        self.visual.preview(index);
        self.visual.update();
    def addCourse(self, args):
        index = self.pool.currentIndex();
        info = courseInfo[index];
        item = QListWidgetItem(info['code']+' :'+info['title'])
        item.setData(Qt.UserRole,index);
        self.myCourses.addItem(item);
        self.visual.addCourse(index);
    def removeCourse(self):
        index = self.myCourses.currentItem().data(Qt.UserRole);
        self.myCourses.takeItem(self.myCourses.currentRow());
        self.visual.removeCourse(index);
    def clear(self):
        self.myCourses.clear();
        self.visual.clear();
    def closeEvent(self,event):
        self.visual.close();
        super(OS_GUI,self).closeEvent(event);

if __name__ == "__main__":
    app = QApplication(sys.argv);
    w = OS_GUI();
    w.setWindowTitle('OlinScheduler');
    w.show();
    sys.exit(app.exec_());
