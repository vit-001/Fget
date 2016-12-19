__author__ = 'Vit'

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import (QPainter)
from PyQt5.QtWidgets import (QWidget)


class QVScroll(QWidget):
    def __init__(self, parent=None, line_width=4, scroller_width=8, delta=1):
        QWidget.__init__(self, parent)
        self.lw = line_width
        self.sw = scroller_width
        self.dx = delta
        self.max = 1
        self.low = 0
        self.l = 0

    def set_values(self, low_value, lenght):
        # print('set_values',low_value,lenght)
        self.low = low_value
        self.l = lenght
        self.update()

    def set_max(self, value):
        # print('set_max',value)
        self.max = value
        self.update()

    def minimumSizeHint(self):
        return QSize(self.sw, 100)

    def sizeHint(self):
        return QSize(self.sw, 100)

    def paintEvent(self, event):
        # print(event.rect())
        geometry = self.geometry()
        painter = QPainter(self)

        line = QRect(self.sw - self.dx - self.lw - 1, 0, self.lw, geometry.height() - 1)
        painter.setBrush(Qt.lightGray)
        painter.setPen(Qt.lightGray)
        painter.drawRect(line)

        if self.max == 0: return
        if self.l == 0: return

        min = self.low * self.geometry().height() // self.max
        l = int(self.l * self.size().height())
        if min + l > geometry.height() - 1: l = geometry.height() - 1 - min

        # print('paintEvent',min,l)

        scroller = QRect(0, min, self.sw - 1, l)
        # print(scroller)
        painter.setBrush(Qt.gray)
        painter.setPen(Qt.gray)
        painter.drawRect(scroller)
