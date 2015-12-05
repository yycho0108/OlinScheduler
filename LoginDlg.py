from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic

import getCourseInfo

class LoginDlg(QDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent);
        uic.loadUi("LoginDlg.ui",self);
        #self.termBox.addItem('SP');
        #self.termBox.addItem('FA');
    def accept(self):
        logID = str(self.idEdit.text());
        logPW = str(self.pwEdit.text());
        Sem = str(self.yearBox.value()) + ';' + str(self.termBox.currentText());
        getCourseInfo.getCourseInfo(logID,logPW,Sem);
        QDialog.accept(self);
    def reject(self):
        QDialog.reject(self);
