# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Dropbox/Hobby/PRG/PyWork/FGet/view/ui/favorite_line_ui.ui'
#
# Created: Wed Mar 25 17:24:43 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_favorite_line(object):
    def setupUi(self, favorite_line):
        favorite_line.setObjectName("favorite_line")
        favorite_line.resize(673, 22)
        favorite_line.setFrameShape(QtWidgets.QFrame.StyledPanel)
        favorite_line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout = QtWidgets.QGridLayout(favorite_line)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.bn_add = QtWidgets.QToolButton(favorite_line)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bn_add.sizePolicy().hasHeightForWidth())
        self.bn_add.setSizePolicy(sizePolicy)
        self.bn_add.setObjectName("bn_add")
        self.gridLayout.addWidget(self.bn_add, 0, 0, 1, 1)
        self.bn_del = QtWidgets.QToolButton(favorite_line)
        self.bn_del.setEnabled(True)
        self.bn_del.setObjectName("bn_del")
        self.gridLayout.addWidget(self.bn_del, 0, 1, 1, 1)
        self.combo_category = QtWidgets.QComboBox(favorite_line)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_category.sizePolicy().hasHeightForWidth())
        self.combo_category.setSizePolicy(sizePolicy)
        self.combo_category.setEditable(True)
        self.combo_category.setObjectName("combo_category")
        self.gridLayout.addWidget(self.combo_category, 0, 2, 1, 1)
        self.combo_url = QtWidgets.QComboBox(favorite_line)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_url.sizePolicy().hasHeightForWidth())
        self.combo_url.setSizePolicy(sizePolicy)
        self.combo_url.setObjectName("combo_url")
        self.gridLayout.addWidget(self.combo_url, 0, 3, 1, 1)
        self.bn_go = QtWidgets.QToolButton(favorite_line)
        self.bn_go.setObjectName("bn_go")
        self.gridLayout.addWidget(self.bn_go, 0, 4, 1, 1)

        self.retranslateUi(favorite_line)
        QtCore.QMetaObject.connectSlotsByName(favorite_line)

    def retranslateUi(self, favorite_line):
        _translate = QtCore.QCoreApplication.translate
        favorite_line.setWindowTitle(_translate("favorite_line", "Frame"))
        self.bn_add.setText(_translate("favorite_line", "+"))
        self.bn_del.setText(_translate("favorite_line", "-"))
        self.bn_go.setText(_translate("favorite_line", "   GO   "))

