__author__ = 'Vit'

__all__ = ['QThumbViewVS']

from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

from view.qt_ui.scroll_bar_widget_ui import Ui_ScrollBarWidget
from view.qt_widget.qt_annotated_button import QAnnotatedButton


class QThumbView(QWidget):
    def __init__(self, parent=None, scroller=None, thumb_size=200, space=2):
        QWidget.__init__(self, parent)
        self.space = space
        self.thumb_size = thumb_size
        self.spacing = self.thumb_size + self.space
        self.coloumns = 1
        self.thumbs = list()
        self.text_visible = False
        self.speed = self.spacing // 2
        self.saved_scroll = None
        self.scroller = scroller
        self.scroller.valueChanged.connect(self.on_scroll)
        self._scroller_setup()

    def add(self, pix_fname='', action=lambda: None, popup='',labels:list=''):
        button = QAnnotatedButton(self, labels)
        button.setAutoRaise(True)
        # if self.text_visible:
        #     button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #     thumb_h = self.thumb_size * 87 / 100
        # else:
        #     button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        #     thumb_h = self.thumb_size
        # button.setLabels(labels)
        button.clicked.connect(action)
        button.setFixedSize(self.thumb_size, self.thumb_size)

        pixmap = QPixmap(pix_fname)
        icon = QIcon()
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QSize(self.thumb_size, self.thumb_size))
        button.setToolTip(popup)

        self.thumbs.append(button)
        self._place()
        self._scroller_set_max()

    def clear(self):
        for item in self.thumbs:
            item.setParent(None)
            item.clicked.disconnect()
            item.close()
        self.thumbs = list()
        self._scroller_set_max()

    @property
    def count(self):
        return len(self.thumbs)

    def minimumSizeHint(self):
        return QSize(self.thumb_size + 2 * self.space, self.thumb_size + 2 * self.space)

    def sizeHint(self):
        return QSize(self.thumb_size + 2 * self.space, self.thumb_size + 2 * self.space)

    def _place(self):
        base = -self.scroller.value()
        i = 0
        for item in self.thumbs:
            x = self.spacing * (i % self.coloumns)
            y = self.spacing * (i // self.coloumns) + base
            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            item.show()
            i += 1

    def _scroller_setup(self):
        self.scroller.setMinimum(0)

        self.scroller.setPageStep(self.size().height() // self.spacing * self.spacing)
        self.scroller.setSingleStep(self.spacing // 2)
        self._scroller_set_max()

    def _scroller_set_max(self):
        thumbs = len(self.thumbs)
        if thumbs % self.coloumns == 0:
            rows = thumbs // self.coloumns
        else:
            rows = thumbs // self.coloumns + 1
        curr_max = max(rows * self.spacing - self.size().height(), 0)
        self.scroller.setMaximum(curr_max)
        if self.saved_scroll is not None and curr_max >= self.saved_scroll:
            self.scroller.setValue(self.saved_scroll)
            self.saved_scroll = None

    def wheelEvent(self, event):
        self.scroller.setValue(self.scroller.value() - event.angleDelta().y() // 120 * self.speed)

    def on_scroll(self, value):
        self._place()

    def resizeEvent(self, event):
        size = event.size()
        col = size.width() // self.spacing
        if col == 0:
            col = 1
        if self.coloumns != col:
            new_scroll_value = self.scroller.value() * self.coloumns // col
            self.coloumns = col
            self._scroller_setup()
            self.scroller.setValue(new_scroll_value)
            self._place()

    def set_thumb_text_visible(self, visible=False):
        self.text_visible = visible


class QThumbViewVS(QWidget):
    def __init__(self, parent=None, Qt_WindowFlags_flags=0, size=200, space=2):
        QWidget.__init__(self, parent)

        self.ui = Ui_ScrollBarWidget()
        self.ui.setupUi(self)

        self.thumbs = QThumbView(parent=self.ui.area, scroller=self.ui.scroll_bar, thumb_size=size, space=space)
        self.ui.area_layout.addWidget(self.thumbs)

    def add(self, pix_fname='', action=lambda: None, popup='',labels=''):
        self.thumbs.add(pix_fname, action, popup, labels)

    def clear(self):
        self.thumbs.clear()

    @property
    def count(self):
        return self.thumbs.count

    @property
    def context(self):
        return self.ui.scroll_bar.value()

    @context.setter
    def context(self, value):
        if value is not None:
            self.thumbs.saved_scroll = value

    def set_thumb_text_visible(self, visible=False):
        self.thumbs.set_thumb_text_visible(visible)
