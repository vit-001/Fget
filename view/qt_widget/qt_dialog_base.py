__author__ = 'Nikitin'

from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from view.qt_ui.dialog_base_ui import Ui_DialogBase


class DialogBase(QDialog):
    def __init__(self, QWidget_parent=None, Qt_WindowFlags_flags=QtCore.Qt.Dialog):
        super().__init__(QWidget_parent, Qt_WindowFlags_flags)

        self.ui = Ui_DialogBase()
        self.ui.setupUi(self)
