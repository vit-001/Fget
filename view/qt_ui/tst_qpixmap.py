# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Dropbox/Hobby/PRG/PyWork/FGet/view/ui/tst_qpixmap.ui'
#
# Created: Wed Jan 28 01:23:08 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1298, 1123)
        self.main = QtWidgets.QWidget(MainWindow)
        self.main.setObjectName("main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../files/photo.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.toolButton = QtWidgets.QToolButton(self.main)
        self.toolButton.setMouseTracking(False)
        self.toolButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.toolButton.setAutoFillBackground(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../files/photo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(200, 200))
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout.addWidget(self.toolButton)
        MainWindow.setCentralWidget(self.main)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1298, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>sdkvlskvlksvn</p></body></html>", "xxx"))
        self.toolButton.setText(_translate("MainWindow", "..."))

