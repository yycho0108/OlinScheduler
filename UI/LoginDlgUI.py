# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginDlg.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(245, 166)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 130, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.splitter_4 = QtGui.QSplitter(Dialog)
        self.splitter_4.setGeometry(QtCore.QRect(20, 10, 211, 101))
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName(_fromUtf8("splitter_4"))
        self.splitter_3 = QtGui.QSplitter(self.splitter_4)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.label = QtGui.QLabel(self.splitter_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.splitter_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.splitter_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.splitter_2 = QtGui.QSplitter(self.splitter_4)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.idEdit = QtGui.QLineEdit(self.splitter_2)
        self.idEdit.setObjectName(_fromUtf8("idEdit"))
        self.pwEdit = QtGui.QLineEdit(self.splitter_2)
        self.pwEdit.setObjectName(_fromUtf8("pwEdit"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.yearBox = QtGui.QSpinBox(self.splitter)
        self.yearBox.setMinimum(0)
        self.yearBox.setMaximum(9999)
        self.yearBox.setProperty("value", 2016)
        self.yearBox.setObjectName(_fromUtf8("yearBox"))
        self.termBox = QtGui.QComboBox(self.splitter)
        self.termBox.setObjectName(_fromUtf8("termBox"))
        self.termBox.addItem(_fromUtf8(""))
        self.termBox.addItem(_fromUtf8(""))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "ID:", None))
        self.label_2.setText(_translate("Dialog", "PW:", None))
        self.label_3.setText(_translate("Dialog", "Term", None))
        self.termBox.setItemText(0, _translate("Dialog", "FA", None))
        self.termBox.setItemText(1, _translate("Dialog", "SP", None))

