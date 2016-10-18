from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from base_classes import AbstractViewManager
from view.qt_ui.tool_box_ui import Ui_ToolBox
from view.qt_fav_change_dlg import FavoriteChangeDialog

__author__ = 'Vit'


class ToolBox(QMainWindow):
    def __init__(self, parent=None, view_manager=AbstractViewManager):
        QMainWindow.__init__(self, parent)
        self.manager=view_manager
        self.controller = view_manager.get_controller()
        self.favorites = self.controller.get_favorites()
        self.favorites.add_listener(self.on_fav_changed)
        self.ui = Ui_ToolBox()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.edit=None

        self.move(40, 985)
        self.bind_all()

        self.action_thumb_filter = QAction("Show thumbnail page", self, checkable=True, triggered=self.url_combo_load)
        self.action_thumb_filter.setChecked(True)

        self.action_pix_filter = QAction("Show pictures page", self, checkable=True, triggered=self.url_combo_load)
        self.action_pix_filter.setChecked(True)

        self.action_video_filter = QAction("Show video page", self, checkable=True, triggered=self.url_combo_load)
        self.action_video_filter.setChecked(True)

        menu = QMenu(self)
        menu.addAction(self.action_thumb_filter)
        menu.addAction(self.action_pix_filter)
        menu.addAction(self.action_video_filter)
        self.ui.bn_filter.setMenu(menu)

        self.curr_urls = list()
        self.category_combo_load()

    def bind_all(self):
        self.ui.combo_category.currentIndexChanged.connect(self.url_combo_load)
        self.ui.bn_go.clicked.connect(
            lambda: self.controller.goto_url(self.curr_urls[self.ui.combo_url.currentIndex()].url))
        self.ui.bn_edit.clicked.connect(self.favorite_edit)
        self.ui.bn_add_thumb.clicked.connect(self.add_thumb)
        self.ui.bn_add_page.clicked.connect(self.add_full)
        self.ui.bn_config.clicked.connect(self.manager.show_config_dialog)

    def panic(self):
        self.hide()
        if self.edit is not None:
            self.edit.hide()

    def add_thumb(self):
        self.controller.add_thumb_page_to_fav(self.ui.combo_category.currentText())

    def add_full(self):
        self.controller.add_full_page_to_fav(self.ui.combo_category.currentText())

    def favorite_edit(self):
        curr_record = self.curr_urls[self.ui.combo_url.currentIndex()]
        self.edit = FavoriteChangeDialog(None, curr_record, self.favorites)
        # self.edit.addAction(self.panic_action)
        self.edit.show()

    def on_fav_changed(self,record):
        if record is None:
            save_cat_index=self.ui.combo_category.currentIndex()
            save_url_index=self.ui.combo_url.currentIndex()

            self.category_combo_load()
            self.ui.combo_category.setCurrentIndex(save_cat_index)

            self.url_combo_load()
            self.ui.combo_url.setCurrentIndex(save_url_index)
        else:
            self.category_combo_load()
            self.ui.combo_category.setCurrentText(record.category)
            self.url_combo_load()
            self.ui.combo_url.setCurrentText(record.combo_view)

    def category_combo_load(self):
        self.ui.combo_category.clear()
        self.ui.combo_category.addItems(self.favorites.get_categories())

    # def connect_to(self, tool_button):
    #     self.tb = tool_button
    #     tool_button.clicked.connect(self.on_clicked_show)
    #
    # def on_clicked_show(self):
    #     if self.isHidden():
    #         self.show()
    #     else:
    #         self.hide()

    def url_combo_load(self):
        fav_list = self.favorites.get(self.ui.combo_category.currentText())
        self.ui.combo_url.clear()
        self.curr_urls = list()
        for item in fav_list:
            if self.url_filter(item):
                self.ui.combo_url.addItem(item.combo_view)
                self.curr_urls.append(item)

    def url_filter(self,item):
        if self.action_thumb_filter.isChecked():
            if item.is_thumb(): return True
        if self.action_pix_filter.isChecked():
            if item.is_pix(): return True
        if self.action_video_filter.isChecked():
            if item.is_video(): return True
        return False

    def addAction(self, action):
        super().addAction(action)
        self.panic_action=action




