# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton,QWidget,QPushButton,QLayout,QSizePolicy,QApplication,QVBoxLayout,QLabel

class QAnnotatedButton(QToolButton):

    def __init__(self, QWidget_parent=None):
        super().__init__(QWidget_parent)

        label1=QLabel(self)
        label1.setText('')
        label1.setAlignment(Qt.AlignTop | Qt.AlignRight)
        label1.setMargin(5)
        self.label_top=label1

        label2=QLabel(self)
        label2.setText('')
        label2.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        label2.setMargin(5)
        self.label_bottom=label2



    def setFixedSize(self, *__args):
        super().setFixedSize(*__args)
        self.label_top.setFixedSize(*__args)
        self.label_bottom.setFixedSize(*__args)

    def setTextTop(self, p_str):
        self.label_top.setText(p_str)

    def setTextBottom(self, p_str):
        self.label_bottom.setText(p_str)


if __name__ == "__main__":

    class Window(QWidget):
        def __init__(self):

            super(Window, self).__init__()
            self.thumb_size=150

            layout = QVBoxLayout()

            button1 = QAnnotatedButton()
            button1.setAutoRaise(True)
            button1.setText('testtesttest')
            button1.setTextBottom('bottom')
            button1.setTextTop('top')
            button1.setFixedSize(self.thumb_size, self.thumb_size) #E:\repo\fget\view\qt_ui\files\picture
            button1.setToolTip('popup')

            pixmap = QPixmap('E:/repo/fget/view/qt_ui/files/picture/logo.png')
            icon = QIcon()
            icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
            button1.setIcon(icon)
            button1.setIconSize(QSize(self.thumb_size, self.thumb_size))


            button2 = QAnnotatedButton()
            button2.setAutoRaise(True)
            button2.setText('testtesttest')
            button2.setFixedSize(self.thumb_size, self.thumb_size)
            button2.setToolTip('popup')


            layout.addWidget(button1)
            layout.addWidget(button2)

            self.setLayout(layout)

            self.setWindowTitle("Test")


    import sys

    app = QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
