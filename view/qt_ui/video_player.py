# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Dropbox/Hobby/PRG/PyWork/FGet/view/ui/video_player.ui'
#
# Created: Wed Jan 28 01:23:09 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_VideoPlayer(object):
    def setupUi(self, VideoPlayer):
        VideoPlayer.setObjectName("VideoPlayer")
        VideoPlayer.resize(438, 447)
        self.centralwidget = QtWidgets.QWidget(VideoPlayer)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mid_frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mid_frame.sizePolicy().hasHeightForWidth())
        self.mid_frame.setSizePolicy(sizePolicy)
        self.mid_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mid_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mid_frame.setObjectName("mid_frame")
        self.mid_frame_layout = QtWidgets.QHBoxLayout(self.mid_frame)
        self.mid_frame_layout.setObjectName("mid_frame_layout")
        self.verticalLayout.addWidget(self.mid_frame)
        self.bottom_frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_frame.sizePolicy().hasHeightForWidth())
        self.bottom_frame.setSizePolicy(sizePolicy)
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom_frame.setObjectName("bottom_frame")
        self.bottom_frame_layout = QtWidgets.QHBoxLayout(self.bottom_frame)
        self.bottom_frame_layout.setObjectName("bottom_frame_layout")
        self.bn_go = QtWidgets.QToolButton(self.bottom_frame)
        self.bn_go.setObjectName("bn_go")
        self.bottom_frame_layout.addWidget(self.bn_go)
        self.verticalLayout.addWidget(self.bottom_frame)
        VideoPlayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VideoPlayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 438, 21))
        self.menubar.setObjectName("menubar")
        VideoPlayer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VideoPlayer)
        self.statusbar.setObjectName("statusbar")
        VideoPlayer.setStatusBar(self.statusbar)

        self.retranslateUi(VideoPlayer)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayer)

    def retranslateUi(self, VideoPlayer):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayer.setWindowTitle(_translate("VideoPlayer", "MainWindow"))
        self.bn_go.setText(_translate("VideoPlayer", "GO"))
