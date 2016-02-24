#!/usr/bin/python3

#built-in modules
import sys
import pickle

#QT modules
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#custom modules
import globalVar
from CourseObject import *
from CourseEntryDlg import *
from LoginDlg import *

from UI.MainWindowUI import Ui_MainWindow


def detectCollision(i_1,i_2): #two indices
    mp_1_list = globalVar.courseInfo[i_1]['meetingPattern']; #list of meetings
    mp_2_list = globalVar.courseInfo[i_2]['meetingPattern'];
    for mp_1 in mp_1_list:
        for mp_2 in mp_2_list:
            if mp_1['day'] is mp_2['day']:
                t_1 = mp_1['time'];
                t_2 = mp_2['time'];
                if not (t_1[1]<t_2[0] or t_2[1]<t_1[0]):
                    return True;
    return False;

class ScheduleView(QGraphicsView):
    def __init__(self, scene,mainWindow):
        self.mainWindow = mainWindow;
        QGraphicsView.__init__(self,scene);
        self.myScene = scene;
        self.resize(500,800);
        self.setWindowTitle('schedule');
        self.prevCourse = None;
        self.courseList = [];
        self.setMouseTracking(True);
    def closeEvent(self,event):
        self.mainWindow.clear();
        super(ScheduleView,self).closeEvent(event);
    def updateDisplay(self):
        # when opts change
        # example placeholder code
        print('here');
    def clear(self):
        for c in self.courseList:
            c.clear();
        self.courseList = [];
    def save(self):
        QPixmap.grabWidget(self).save('schedule.png');
    def preview(self,i):
        if self.prevCourse is not None:
            self.prevCourse.clear();
        self.prevCourse = CourseObject(parent=self,index=i);
        self.prevCourse.resize(self.width(),self.height());
    def selectCourse(self,i):
        cCol = QColor.fromRgb(0,0,0,255);
        self.prevCourse.setFrameColor(cCol);
        self.courseList.append(self.prevCourse);
        self.prevCourse = None;

    def removeCourse(self,i):
        targList = filter(lambda c : c.index == i, self.courseList);
        for c in targList:
            c.clear();
            self.courseList.remove(c);
            break;
    def setCourseColor(self,i,col):
        targList = filter(lambda c : c.index == i, self.courseList);
        for c in targList:
            c.setBkColor(col);
    def paintEvent(self,event):
        QGraphicsView.paintEvent(self,event);
        q = QPainter(self.viewport());
        w = self.width(); #5 days + 1(left) for axis labels
        h = self.height(); # 12 hours + 1(top) for axis labels
        myColor = QColor.fromRgbF(0.5,0.4,0.3,0.3);
        myPen = QPen(myColor);
        q.setPen(myPen);
        for i in range(0,6):
            for j in range(0,13):
                q.drawRect(i*w/6,j*h/13,w/6,h/13);
                if i == 0 and j != 0:
                    q.drawText(i*w/6,j*h/13,w/6,h/13,Qt.AlignTop|Qt.AlignHCenter,str(8+j)+":00");
                elif j == 0:
                    days = ['','Monday','Tuesday','Wednesday','Thursday','Friday'];
                    q.drawText(i*w/6,j*h/13,w/6,h/13,Qt.AlignVCenter|Qt.AlignHCenter,days[i]);

    def resizeEvent(self,event):
        w = self.width();
        h = self.height();
        if self.prevCourse is not None:
            self.prevCourse.resize(w,h);
        for c in self.courseList:
            c.resize(w,h);
        QGraphicsView.resizeEvent(self,event);
    #def mouseMoveEvent(self,event):
    #    QGraphicsView.mouseMoveEvent(self,event);
    #    print('move');
    #    pass;


class OS_GUI(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent);
        self.setupUi(self)
        self.pool.activated.connect(self.onBrowseClass);
        self.visual = None;
        self.onOpenSchedule();
        self.selectBtn.clicked.connect(self.selectCourse);
        self.newBtn.clicked.connect(self.newCourse);
        self.deleteBtn.clicked.connect(self.deleteCourse);
        self.removeBtn.clicked.connect(self.removeCourse);
        self.clearBtn.clicked.connect(self.clear);
        self.openSchedule.clicked.connect(self.onOpenSchedule);
        self.actionTitle.triggered.connect(self.visual.updateDisplay);
        self.actionCourses.triggered.connect(self.saveCourses);
        self.actionSchedule.triggered.connect(self.saveSchedule);
        self.colorBtn.clicked.connect(self.setCourseColor);
        self.loadData();
        self.onBrowseClass(self.pool.currentIndex()); #in order to avoid selecting w/o preview
    def loadData(self):
        try:
            with open('course.olin', 'rb') as f_in:
                self.pool.blockSignals(True);
                self.pool.clear();
                globalVar.courseInfo = pickle.load(f_in);
                for course in globalVar.courseInfo:
                    self.pool.addItem(course['title']);
                self.pool.blockSignals(False);
        except IOError:
            reply = QMessageBox.question(self,"Course Data Not Found","Initialize Database(course.olin)?", QMessageBox.Yes|QMessageBox.No);
            global app;
            if reply == QMessageBox.Yes:
                d = LoginDlg(parent=self);
                if d.exec_() == QDialog.Rejected:
                    raise;
                else:
                    # established data pool
                    self.loadData();
            else:
                raise;
    def saveCourses(self):
        with open("course.olin","wb") as out:
            pickle.dump(globalVar.courseInfo,out,pickle.HIGHEST_PROTOCOL);
    def saveSchedule(self):
        self.visual.save();
    def onOpenSchedule(self):
        if self.visual is not None:
            self.clear();
            self.visual.deleteLater();
        self.visual = ScheduleView(QGraphicsScene(self),self); #beware: not a parent
        self.visual.show();
    def onBrowseClass(self, index):
        info = globalVar.courseInfo[index];
        self.code.setText(info['code']);
        self.title.setText(info['title']);
        self.instructors.clear();
        self.instructors.addItems(info['instructor']);
        self.credit.setText(info['credit']);
        #self.myCourses.model().insertRow(3);
        #qm.setData(qm.rowCount(), info['code'] + ' : ' + info['title']);
        self.visual.preview(index);
        self.visual.update();
    def newCourse(self,args):
        d = CourseEntryDlg(parent=self);
        if d.exec_() == QDialog.Rejected:
            print('rejected');
        else:
            course = d.getClass();
            globalVar.courseInfo.append(course);
            self.pool.addItem(course['title']);
    def deleteCourse(self,args):
        reply = QMessageBox.question(self,"Warning","Are you sure you want to remove this course?",QMessageBox.Yes|QMessageBox.No);
        if reply == QMessageBox.Yes:
            i = self.pool.currentIndex();
            self.pool.removeItem(i);
            del globalVar.courseInfo[i];
    def selectCourse(self, args):
        i_new = self.pool.currentIndex();
        for i in range(self.myCourses.count()):
            i_old = self.myCourses.item(i).data(Qt.UserRole);
            if detectCollision(i_new,i_old):
                #ask user for confirmation
                reply = QMessageBox.question(self,"Collision Detected","Some courses collide in your schedule. continue?", QMessageBox.Yes|QMessageBox.No);
                if reply == QMessageBox.No:
                    return;
                else: #the user clearly doesn't care
                    break;
        info = globalVar.courseInfo[i_new];
        item = QListWidgetItem(info['code']+' :'+info['title'])
        item.setData(Qt.UserRole,i_new);
        #item.setBackgroundColor(QColor.fromRgbF(0.5,0.5,0,0.5));
        self.myCourses.addItem(item);
        self.visual.selectCourse(i_new);
    def removeCourse(self):
        index = self.myCourses.currentItem().data(Qt.UserRole);
        self.myCourses.takeItem(self.myCourses.currentRow());
        self.visual.removeCourse(index);
    def setCourseColor(self):
        col = QColorDialog.getColor();
        if col.isValid():
            item = self.myCourses.currentItem();
            index = item.data(Qt.UserRole);
            item.setBackgroundColor(col);
            self.visual.setCourseColor(index,col);
    def clear(self):
        self.myCourses.clear();
        self.visual.clear();
    def closeEvent(self,event):
        self.visual.close();
        super(OS_GUI,self).closeEvent(event);

if __name__ == "__main__":
    global app;
    app = QApplication(sys.argv);
    w = OS_GUI();
    w.setWindowTitle('OlinScheduler');
    w.show();
    w.loadData();
    sys.exit(app.exec_());
