# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Dropbox/Hobby/PRG/PyWork/FGet/view/ui/fav_change_dialog_ui.ui'
#
# Created: Wed Mar 25 17:24:43 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_EditDialog(object):
    def setupUi(self, EditDialog):
        EditDialog.setObjectName("EditDialog")
        EditDialog.resize(392, 188)
        EditDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(EditDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.input_name = QtWidgets.QLineEdit(self.frame)
        self.input_name.setObjectName("input_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_name)
        self.check_delete = QtWidgets.QCheckBox(self.frame)
        self.check_delete.setObjectName("check_delete")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.check_delete)
        self.combo_category = QtWidgets.QComboBox(self.frame)
        self.combo_category.setEditable(False)
        self.combo_category.setObjectName("combo_category")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.combo_category)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.input_url = QtWidgets.QLineEdit(self.frame)
        self.input_url.setEnabled(False)
        self.input_url.setText("")
        self.input_url.setReadOnly(True)
        self.input_url.setObjectName("input_url")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_url)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.input_type = QtWidgets.QLineEdit(self.frame)
        self.input_type.setEnabled(False)
        self.input_type.setReadOnly(True)
        self.input_type.setObjectName("input_type")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_type)
        self.verticalLayout.addWidget(self.frame)
        self.buttons_ok_cancel = QtWidgets.QDialogButtonBox(EditDialog)
        self.buttons_ok_cancel.setOrientation(QtCore.Qt.Horizontal)
        self.buttons_ok_cancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttons_ok_cancel.setObjectName("buttons_ok_cancel")
        self.verticalLayout.addWidget(self.buttons_ok_cancel)

        self.retranslateUi(EditDialog)
        self.buttons_ok_cancel.accepted.connect(EditDialog.accept)
        self.buttons_ok_cancel.rejected.connect(EditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditDialog)

    def retranslateUi(self, EditDialog):
        _translate = QtCore.QCoreApplication.translate
        EditDialog.setWindowTitle(_translate("EditDialog", "Edit/delete favorite"))
        self.label.setText(_translate("EditDialog", "Name"))
        self.check_delete.setText(_translate("EditDialog", "Delete from favorites"))
        self.label_2.setText(_translate("EditDialog", "Category"))
        self.label_3.setText(_translate("EditDialog", "URL"))
        self.label_4.setText(_translate("EditDialog", "Type"))
