from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#UI
from UI.CourseEntryDlgUI import Ui_CourseEntryDlg

def dayToDay(d):
    if str is 'Thursday':
        return 'R';
    else:
        return d[0];

class CourseEntryDlg(QDialog,Ui_CourseEntryDlg):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent);
        #uic.loadUi("CourseEntryDlg.ui",self);
        self.setupUi(self)
        self.addBtn.clicked.connect(self.addMP);
        self.MPTable.setHorizontalHeaderLabels(["Day","Time","Loc"]);
        self.instAddBtn.clicked.connect(self.addInst);
        #self.MPTable.
    def addInst(self):
        self.instList.addItem(self.instEdit.text());
        self.instEdit.clear();
    def addMP(self):
        location = str(self.locEdit.text());
        
        tStart = self.tStartEdit.time(); #QTime
        tEnd = self.tEndEdit.time();
        day = self.dayCombo.currentText();
        row = self.MPTable.rowCount();
        self.MPTable.setRowCount(row+1);

        d = QTableWidgetItem(day);
        d.setData(Qt.UserRole, dayToDay(day));
        t = QTableWidgetItem(tStart.toString("h:mm AP") + " - " + tEnd.toString("h:mm AP"));
        t.setData(Qt.UserRole,[60*tStart.hour()+tStart.minute(), 60*tEnd.hour()+tEnd.minute()]);
        l = QTableWidgetItem(location);
        l.setData(Qt.UserRole,location);
        
        self.MPTable.setItem(row,0,d);
        self.MPTable.setItem(row,1,t);
        self.MPTable.setItem(row,2,l);

    def getClass(self):
        instructor = [];
        for i in range(self.instList.count()):
            instructor.append(self.instList.item(i).text());
        mp = [];
        for i in range(self.MPTable.rowCount()):
            mp.append({
                'day':self.MPTable.item(i,0).data(Qt.UserRole),
                'time':self.MPTable.item(i,1).data(Qt.UserRole),
                'loc':self.MPTable.item(i,2).data(Qt.UserRole)
                });
        
        return {
            "code" : self.codeEdit.text(),
            "title" : self.titleEdit.text(),
            "instructor" : instructor,
            "openSpots" : 'N/A',
            "status" : 'N/A', #added manually anyways
            "meetingPattern" : mp,
            "credit" : self.creditEdit.text()
        };
