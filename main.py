import pickle

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
import getCourseInfo

import globalVar
from courseDisplay import *

RECT_TYPE = 3;
TEXT_TYPE = 8;

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
        # when opts change
        # example placeholder code
        print('here');
    def clear(self):
        self.myScene.clear();
    def save(self):
        QPixmap.grabWidget(self).save('schedule.png');
    def preview(self,i):
        if self.prevCourse is not None:
            self.prevCourse.clear();
        self.prevCourse = courseDisplay(parent=self,index=i);
    def addCourse(self,i):
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
        try:
            with open('wrongInfo.dat', 'rb') as f_in:
                self.pool.blockSignals(True);
                self.pool.clear();
                globalVar.courseInfo = pickle.load(f_in);
                for course in globalVar.courseInfo:
                    # make numeric
                    # course['meetingPattern'] = parseMeet(course['meetingPattern']);
                    self.pool.addItem(course['title']);
                self.pool.blockSignals(False);
        except IOError:
            reply = QMessageBox.question(self,"Course Data Not Found","Initialize Database(courseInfo.dat)?", QMessageBox.Yes|QMessageBox.No);
            if reply == QMessageBox.Yes:
                d = QDialog(self);
                uic.loadUi("credentials.ui",d);
                d.exec_();
                pass;#reinitialize
            else:
                pass;
    def onOpenSchedule(self):
        self.visual = scheduleView(QGraphicsScene(self),self); #beware: not a parent
        self.visual.show();
    def onSelectClass(self, index):
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
    def addCourse(self, args):
        index = self.pool.currentIndex();
        info = globalVar.courseInfo[index];
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
