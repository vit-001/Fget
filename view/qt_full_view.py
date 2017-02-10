from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QFrame

from base_classes import AbstractFullView, AbstractViewManager
from view.qt_ui.favorite_line_ui import Ui_favorite_line
from view.qt_ui.full_view_base_ui import Ui_FullView
from view.qt_widget.qt_button_line import QButtonLine

__author__ = 'Vit'


class FullView(QMainWindow, AbstractFullView):
    def __init__(self, parent=None, view_manager=AbstractViewManager):
        QMainWindow.__init__(self, parent)
        self.manager = view_manager
        self.controller = view_manager.get_controller()

        self.url = None

        self.ui = Ui_FullView()
        self.ui.setupUi(self)

        self.controls = QButtonLine(self.ui.bottom_frame)
        self.ui.bottom_frame_layout.addWidget(self.controls, 0, 0)

        self.ui.bottom_frame_layout.setColumnStretch(0, 1)
        self.ui.bottom_frame_layout.setColumnStretch(1, 1)

        self.fav_frame = QFrame(self.ui.bottom_frame)
        self.fav = Ui_favorite_line()
        self.fav.setupUi(self.fav_frame)
        self.ui.bottom_frame_layout.addWidget(self.fav_frame, 0, 1)

        self.fav.combo_category.currentIndexChanged.connect(self.url_combo_load)
        self.category_combo_load()
        self.fav.bn_go.clicked.connect(
            lambda: self.controller.goto_url(self.curr_urls[self.fav.combo_url.currentIndex()].url))

    def panic(self):
        self.hide()

    def mouseDoubleClickEvent(self, *args, **kwargs):
        if self.windowState() == QtCore.Qt.WindowNoState:
            self.setWindowState(QtCore.Qt.WindowFullScreen)
        else:
            self.setWindowState(QtCore.Qt.WindowNoState)

    def get_url(self):
        return self.url

    def category_combo_load(self):
        self.fav.combo_category.clear()
        self.fav.combo_category.addItems(self.controller.get_favorites().get_categories())

    def url_combo_load(self):
        fav_list = self.controller.get_favorites().get(self.fav.combo_category.currentText())
        self.fav.combo_url.clear()
        self.curr_urls = list()
        for item in fav_list:
            if self.test_favorite_item(item):
                self.fav.combo_url.addItem(item.combo_view)
                self.curr_urls.append(item)

    def add_control(self, text='', action=lambda: 0):
        self.controls.add_button(text, action)

    def set_favorite_list(self, favorite_list=list()):
        self.fav.combo_url.clear()
        self.fav.combo_url.addItems(favorite_list)

    def set_favorite_handlers(self, add_handler=lambda cat: None, category_change_handler=lambda i: None):
        self.fav.combo_category.currentTextChanged.connect(category_change_handler)
        self.fav.bn_add.clicked.connect(lambda: add_handler(self.fav.combo_category.currentText()))

    def set_favorite_category_list(self, category_list=list()):
        self.fav.combo_category.clear()
        self.fav.combo_category.addItems(category_list)

    def closeEvent(self, *args, **kwargs):
        self.hide()
