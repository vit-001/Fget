import glob
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFrame, QLabel

from base_classes import AbstractPictureView, AbstractViewManager, URL
from setting import Setting
from favorites import FavoriteRecord

from view.qt_full_view import FullView

from view.qt_widget.qt_progress_line import QProgressHLine


class PictureView(FullView, AbstractPictureView):
    def __init__(self, parent=None, view_manager=AbstractViewManager):
        FullView.__init__(self,parent,view_manager)

        self.pix_label=QLabel(self.ui.mid_frame)
        self.pix_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.mid_frame_layout.addWidget(self.pix_label)

        self.progress = QProgressHLine(self.ui.mid_frame)
        self.progress.hide()
        self.progress.new_progress('loaded', QtCore.Qt.gray)
        self.progress.new_progress('current', QtCore.Qt.red)

        self.pix = None
        self._redraw()
        self.dir = None
        self.cur_pix = 0
        self.files = list()
        self.max_pics = 0

    def test_favorite_item(self, item):
        return item.is_pix() or item.is_thumb()

    def get_page_type(self):
        return FavoriteRecord.pix


    def set_dir(self, filedir='', url=URL(), max_pics=12):
        self.dir = filedir
        self.url=url
        self.cur_pix = 0
        self.controls.clear()

        self.max_pics = max_pics
        self.progress.set_max(max_pics - 1)
        self.progress.reset()
        self.progress.show()

        self.update()
        self.refresh()

    def refresh(self):
        if self.dir is None: return
        self.files = glob.glob(self.dir + '*.jpg')
        self.load_pix()

    def load_pix(self):
        if len(self.files) == 0: return
        if len(self.files) >= self.max_pics:
            self.progress.hide()
        self.progress.set_value('loaded', len(self.files) - 1)
        self.pix = QPixmap(self.files[self.cur_pix])
        self._redraw()
        self.setWindowTitle(self.files[self.cur_pix])

    def _redraw(self):
        if self.pix is None: return

        l_rect = self.ui.mid_frame.contentsRect()
        p_rect = self.pix.rect()

        try:
            if l_rect.height() / l_rect.width() < p_rect.height() / p_rect.width():
                pix1 = self.pix.scaledToHeight(l_rect.height(), QtCore.Qt.SmoothTransformation)
            else:
                pix1 = self.pix.scaledToWidth(l_rect.width(), QtCore.Qt.SmoothTransformation)
            self.pix_label.setPixmap(pix1)

        except ZeroDivisionError:
            pass

        self.progress.setGeometry(0, l_rect.height() * 9 // 10,
                                  l_rect.width(), l_rect.height() * 9 // 10 + self.progress.height())

        self.progress.set_value('current', self.cur_pix)
        self.progress.update()
        QtCore.QEventLoop().processEvents(QtCore.QEventLoop.AllEvents)
        self.update()

    def resizeEvent(self, *args, **kwargs):
        self._redraw()

    def wheelEvent(self, event):
        self.cur_pix -= event.angleDelta().y() // 120
        if self.cur_pix < 0: self.cur_pix = 0
        if self.cur_pix > len(self.files) - 1: self.cur_pix = len(self.files) - 1
        self.load_pix()
