__author__ = 'Vit'

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from view.qt_ui.tst_qpixmap import *

#
# class PicButton(QAbstractButton):
#     def __init__(self, pixmap, parent=None):
#         super(PicButton, self).__init__(parent)
#         self.pixmap = pixmap
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.drawPixmap(event.rect(), self.pixmap)
#
#     def sizeHint(self):
#         return self.pixmap.size()

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.pixmap=QtGui.QPixmap("E:/Dropbox/Hobby/PRG/PyWork/FGet/files/photo.jpg")

        self.toolButton = QtWidgets.QToolButton(self.ui.main)
        icon = QtGui.QIcon()
        icon.addPixmap(self.pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(200, 200))
        self.toolButton.setObjectName("toolButton")
        self.ui.verticalLayout.addWidget(self.toolButton)
        self.toolButton.setText("...")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())