__author__ = 'Vit'

from PyQt5.Qt import QFont
from PyQt5.QtCore import QPoint, QRect, QSize
from PyQt5.QtWidgets import *


class QButtonLine(QWidget):
    def __init__(self, parent=None, hight=25, space=2):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.space = space
        self.hight = hight
        self.buttons = list()
        self.buttons_width = self.space * 2
        self.curr_scroll = 0
        self.speed = 40

    def add_button(self, text='', action=lambda: None, menu=None, tooltip='', bold=False, underline=False,
                   autoraise=False):
        button = QToolButton(self)
        button.setText(text)
        font = QFont()
        font.setBold(bold)
        font.setUnderline(underline)
        button.setFont(font)
        button.setAutoRaise(autoraise)
        button.clicked.connect(action)
        button.setFixedHeight(self.hight)
        button.setToolTip(tooltip)

        if menu is not None:
            button.setMenu(menu)
            button.setPopupMode(QToolButton.MenuButtonPopup)

        self.buttons.append(button)
        self._place()
        self.show()

    def clear(self):
        for item in self.buttons:
            item.setParent(None)
            item.clicked.disconnect()
            item.close()
        self.buttons = list()
        self.curr_scroll = 0
        self.hide()

    def minimumSizeHint(self):
        return QSize(0, self.hight + 2 * self.space)

    def sizeHint(self):
        return QSize(0, self.hight + 2 * self.space)

    def _place(self):
        x = self.space + self.curr_scroll * self.speed
        y = self.space
        for item in self.buttons:
            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x += item.sizeHint().width() + self.space
            item.show()
        self.buttons_width = x

    def wheelEvent(self, event):
        delta = event.angleDelta().y() // 120
        if self.buttons_width < self.geometry().width():
            if delta < 0: return
        self.curr_scroll += delta
        if self.curr_scroll > 0: self.curr_scroll = 0
        self._place()
