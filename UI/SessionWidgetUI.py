# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SessionWidget.ui'
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

class Ui_courseObj(object):
    def setupUi(self, courseObj):
        courseObj.setObjectName(_fromUtf8("courseObj"))
        courseObj.resize(94, 92)
        courseObj.setWindowOpacity(0.75)
        courseObj.setAutoFillBackground(True)
        self.frame = QtGui.QFrame(courseObj)
        self.frame.setGeometry(QtCore.QRect(0, 0, 91, 91))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setLineWidth(2)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.title = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.title.setMouseTracking(True)
        self.title.setToolTip(_fromUtf8(""))
        self.title.setWhatsThis(_fromUtf8(""))
        self.title.setScaledContents(True)
        self.title.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.title.setWordWrap(True)
        self.title.setObjectName(_fromUtf8("title"))
        self.verticalLayout_2.addWidget(self.title)
        self.location = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.location.sizePolicy().hasHeightForWidth())
        self.location.setSizePolicy(sizePolicy)
        self.location.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.location.setMouseTracking(True)
        self.location.setScaledContents(True)
        self.location.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.location.setWordWrap(True)
        self.location.setObjectName(_fromUtf8("location"))
        self.verticalLayout_2.addWidget(self.location)
        self.time = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy)
        self.time.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.time.setMouseTracking(True)
        self.time.setToolTip(_fromUtf8(""))
        self.time.setScaledContents(True)
        self.time.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.time.setWordWrap(True)
        self.time.setObjectName(_fromUtf8("time"))
        self.verticalLayout_2.addWidget(self.time)

        self.retranslateUi(courseObj)
        QtCore.QMetaObject.connectSlotsByName(courseObj)

    def retranslateUi(self, courseObj):
        courseObj.setWindowTitle(_translate("courseObj", "Form", None))
        self.title.setText(_translate("courseObj", "Title", None))
        self.location.setText(_translate("courseObj", "Location", None))
        self.time.setText(_translate("courseObj", "Time", None))

