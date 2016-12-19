# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Dropbox/Hobby/PRG/PyWork/FGet/view/ui/dialog_base_ui.ui'
#
# Created: Wed Mar 25 17:24:44 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_DialogBase(object):
    def setupUi(self, DialogBase):
        DialogBase.setObjectName("DialogBase")
        DialogBase.resize(401, 70)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogBase.sizePolicy().hasHeightForWidth())
        DialogBase.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DialogBase)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(DialogBase)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_layout = QtWidgets.QGridLayout(self.frame)
        self.frame_layout.setObjectName("frame_layout")
        self.horizontalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogBase)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogBase)
        self.buttonBox.accepted.connect(DialogBase.accept)
        self.buttonBox.rejected.connect(DialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogBase)

    def retranslateUi(self, DialogBase):
        _translate = QtCore.QCoreApplication.translate
        DialogBase.setWindowTitle(_translate("DialogBase", "Dialog"))
