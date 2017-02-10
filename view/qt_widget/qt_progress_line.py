__author__ = 'Vit'

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import (QPainter)
from PyQt5.QtWidgets import (QWidget)


class QProgressHLine(QWidget):
    def __init__(self, parent=None, height=6):
        QWidget.__init__(self, parent)
        self.h = height
        self.space = 2
        self.names = list()
        self.values = dict()
        self.colors = dict()
        self.max = 1

    def new_progress(self, name='', color=Qt.red):
        self.names.append(name)
        self.values[name] = 0
        self.colors[name] = color

    def set_value(self, name, value):
        self.values[name] = value
        self.update()

    def set_max(self, value):
        self.max = value

    def reset(self):
        for name in self.colors:
            self.values[name] = 0
        self.update()

    def minimumSizeHint(self):
        return QSize(100, self.h + 2 * self.space)

    def sizeHint(self):
        return QSize(100, self.h + 2 * self.space)

    def paintEvent(self, event):
        geometry = self.geometry()
        painter = QPainter(self)

        border = QRect(0, 0, geometry.width() - 1, self.h + 2 * self.space - 1)
        painter.setPen(Qt.gray)
        painter.drawRect(border)

        x_max = geometry.width() - 1 - 2 * self.space

        for name in self.names:
            value = self.values[name]
            painter.setBrush(self.colors[name])
            painter.setPen(self.colors[name])
            rect = QRect(self.space, self.space, value * x_max / self.max, self.h - 1)
            painter.drawRect(rect)
