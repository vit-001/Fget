# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Repository/PyWork/fget/view/ui/thumb_viewer_ui.ui'
#
# Created: Sun Feb 26 17:21:13 2017
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(440, 895)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        MainWindow.setDockNestingEnabled(False)
        self.base = QtWidgets.QWidget(MainWindow)
        self.base.setObjectName("base")
        self.baseVLayout_2 = QtWidgets.QVBoxLayout(self.base)
        self.baseVLayout_2.setSpacing(2)
        self.baseVLayout_2.setContentsMargins(0, 9, 0, 0)
        self.baseVLayout_2.setObjectName("baseVLayout_2")
        self.top_frame = QtWidgets.QFrame(self.base)
        self.top_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame.setObjectName("top_frame")
        self.top_frame_layout = QtWidgets.QVBoxLayout(self.top_frame)
        self.top_frame_layout.setSpacing(2)
        self.top_frame_layout.setContentsMargins(4, 0, 4, 0)
        self.top_frame_layout.setObjectName("top_frame_layout")
        self.baseVLayout_2.addWidget(self.top_frame)
        self.mid_frame = QtWidgets.QFrame(self.base)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mid_frame.sizePolicy().hasHeightForWidth())
        self.mid_frame.setSizePolicy(sizePolicy)
        self.mid_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mid_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mid_frame.setObjectName("mid_frame")
        self.mid_frame_layout = QtWidgets.QHBoxLayout(self.mid_frame)
        self.mid_frame_layout.setSpacing(2)
        self.mid_frame_layout.setContentsMargins(4, 2, 4, 2)
        self.mid_frame_layout.setObjectName("mid_frame_layout")
        self.baseVLayout_2.addWidget(self.mid_frame)
        self.bottom_frame = QtWidgets.QFrame(self.base)
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom_frame.setObjectName("bottom_frame")
        self.bottom_frame_layout = QtWidgets.QVBoxLayout(self.bottom_frame)
        self.bottom_frame_layout.setSpacing(2)
        self.bottom_frame_layout.setContentsMargins(4, 0, 4, 0)
        self.bottom_frame_layout.setObjectName("bottom_frame_layout")
        self.baseVLayout_2.addWidget(self.bottom_frame)
        self.buttons_frame = QtWidgets.QFrame(self.base)
        self.buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttons_frame.setObjectName("buttons_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.buttons_frame)
        self.gridLayout.setObjectName("gridLayout")
        self.combo_history = QtWidgets.QComboBox(self.buttons_frame)
        self.combo_history.setEditable(True)
        self.combo_history.setObjectName("combo_history")
        self.gridLayout.addWidget(self.combo_history, 0, 1, 1, 1)
        self.bn_go = QtWidgets.QToolButton(self.buttons_frame)
        self.bn_go.setObjectName("bn_go")
        self.gridLayout.addWidget(self.bn_go, 0, 2, 1, 1)
        self.bn_toolbox = QtWidgets.QToolButton(self.buttons_frame)
        self.bn_toolbox.setCheckable(False)
        self.bn_toolbox.setAutoRaise(False)
        self.bn_toolbox.setObjectName("bn_toolbox")
        self.gridLayout.addWidget(self.bn_toolbox, 0, 4, 1, 1)
        self.bn_back = QtWidgets.QToolButton(self.buttons_frame)
        self.bn_back.setObjectName("bn_back")
        self.gridLayout.addWidget(self.bn_back, 0, 0, 1, 1)
        self.bn_playlist = QtWidgets.QToolButton(self.buttons_frame)
        self.bn_playlist.setObjectName("bn_playlist")
        self.gridLayout.addWidget(self.bn_playlist, 0, 3, 1, 1)
        self.baseVLayout_2.addWidget(self.buttons_frame)
        MainWindow.setCentralWidget(self.base)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 440, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TGP viewer"))
        self.bn_go.setText(_translate("MainWindow", "GO"))
        self.bn_toolbox.setText(_translate("MainWindow", "..."))
        self.bn_back.setText(_translate("MainWindow", "Back"))
        self.bn_playlist.setText(_translate("MainWindow", "PL"))

