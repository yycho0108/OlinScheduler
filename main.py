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
def parseMeet(mList):
    l = {};
    #duration = namedtuple('duration',['start','end']);
    for meet in mList:
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
                if d not in l:
                    l[d] = [];
                l[d].append([parseTime(start), parseTime(end)]);
            #print("start: ",start, " end : ", end);
        except ValueError: #Invalid/Undetermined Meeting Pattern
            #print(meet);
            pass
    #print(l);
    return l;

class courseWidget(QWidget):
    def __init__(self,width=100,height=100,x=0,y=0,parent=None):
        QWidget.__init__(self,parent);
        uic.loadUi("courseWidget.ui",self);
        self.setTitle("courseTitle");
        self.setLocation("courseLocation");
        self.setAutoFillBackground(True);
        col = QColor.fromRgb(55,99,125,192);
        self.setBkColor(col);
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
        print(args);
        d = QDialog(self);
        uic.loadUi("options.ui",d);
        print(d.exec_());
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
        self.previewGroup = QGraphicsItemGroup(scene=self.myScene);
        self.coursesList = [];
        self.setWindowTitle('schedule');
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
    def getItemList(self,i):
        itemList = [];
        mp = courseInfo[i]['meetingPattern'];
        for day, time in mp.items():
            left = 100*parseDay(day);
            for t in time:
                top = t[0] - 60*9;
                height = t[1]-t[0]; #60px per hour
                tCol = QColor.fromRgb(66,66,128,128);
                r = QRectF(left,top,100,height);
                r = QGraphicsRectItem(r);
                t = QGraphicsTextItem(courseInfo[i]['code']);
                t.setPos(left,top);
                itemList.append(r);
                itemList.append(t);
        return itemList;
    def preview(self,i):
        try:
            for item in self.previewGroup.childItems():
                self.myScene.removeItem(item);
            self.myScene.destroyItemGroup(self.previewGroup);
        except RuntimeError:
            pass;
        tCol = QColor.fromRgb(66,66,128,128);
        tPen = QPen(tCol);
        itemList = self.getItemList(i);
        for item in itemList:
            if(item.type() is TEXT_TYPE):
                item.setDefaultTextColor(tCol);
            else:
                item.setPen(tPen);
        self.previewGroup = self.myScene.createItemGroup(itemList);
    def addCourse(self,i):
        cCol = QColor.fromRgb(0,0,0,255);
        cPen = QPen(cCol);
        itemList = self.getItemList(i);
        for item in itemList:
            item.setData(Qt.UserRole,i);
            if(item.type() is TEXT_TYPE):
                item.setDefaultTextColor(cCol);
            else:
                item.setPen(cPen);
            self.myScene.addItem(item);
    def removeCourse(self,i):
        for item in self.myScene.items():
            if item.data(Qt.UserRole) == i:
                self.myScene.removeItem(item);
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
