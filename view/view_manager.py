__author__ = 'Vit'

import os

from PyQt5 import QtCore
from PyQt5.QtGui import QGuiApplication, QKeySequence
from PyQt5.QtWidgets import *

from base_classes import AbstractViewManager, PresenterFromViewInterface, AbstractFullView
from setting import Setting
from view.config_dialog import ConfigDialog
from view.qt_picture_view import PictureView
from view.qt_playlist_view import QTPlaylistView
from view.qt_thumbnail_view import QTThumbViewer
from view.qt_tool_box import ToolBox
from view.qt_video_view import VideoView


class QTViewManager(AbstractViewManager):
    def __init__(self, controller=PresenterFromViewInterface()):
        self.controller = controller

        print('PyQt version: '+QtCore.qVersion())

        Setting.desktop = QApplication.desktop().screenGeometry()
        if Setting.view_debug: print('Running view on display: ', Setting.desktop)

        self.thumb_view = QTThumbViewer(view_manager=self)
        self.picture_view = PictureView(view_manager=self)
        self.video_view = VideoView(view_manager=self)

        self.tool_box = ToolBox(view_manager=self)
        self.config_dialog = None

        self.playlist = QTPlaylistView(Qt_WindowFlags_flags=QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint,
                                       view_manager=self, player=self.video_view.video_player)

        self.thumb_view.setGeometry(Setting.thumb_view_geometry())
        self.picture_view.setGeometry(Setting.full_view_geometry())
        self.video_view.setGeometry(Setting.full_view_geometry())
        self.tool_box.setGeometry(Setting.tool_box_geometry())
        self.playlist.setGeometry(Setting.playlist_geometry())

        self.picture_view.hide()
        self.video_view.hide()
        self.playlist.hide()

        self.add_keyboard_shortcut(self.thumb_view, 'Ctrl+`', self.controller.panic)
        # self.add_keyboard_shortcut(self.video_view,'Space',lambda: (self.video_view.video_player.little_forvard(30)))
        self.thumb_view.show()

    def add_keyboard_shortcut(self, window, shortcut='', on_pressed=lambda: None):
        action = QAction(window)
        action.setShortcut(QKeySequence(shortcut))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        window.addAction(action)
        action.triggered.connect(on_pressed)

    def get_thumb_view(self):
        return self.thumb_view

    def get_video_view(self):
        return self.video_view

    def get_picture_view(self):
        return self.picture_view

    def get_controller(self):
        return self.controller

    def show_full_view(self, view=AbstractFullView()):
        self.picture_view.hide()
        self.video_view.hide()
        view.show()

    def show_config_dialog(self):
        if self.config_dialog is None:
            self.config_dialog = ConfigDialog(manager=self)
            self.config_dialog.show()
            self.config_dialog.finished.connect(self.on_finished_config_dialog)
        else:
            self.config_dialog.hide()
            self.config_dialog.show()

    def on_finished_config_dialog(self, *i):
        self.config_dialog = None

    def toggle_tool_view(self):
        if self.tool_box.isHidden():
            self.tool_box.show()
        else:
            self.tool_box.hide()

    def toggle_playlist_view(self):
        if self.playlist.isHidden():
            self.playlist.show()
        else:
            self.playlist.hide()

    def panic(self):
        self.video_view.panic()
        self.picture_view.panic()
        self.thumb_view.panic()
        self.tool_box.panic()

    def show_status(self, txt=''):
        self.thumb_view.show_status(txt)

    def on_close_event(self):
        self.picture_view.destroy()
        self.video_view.destroy()
        self.controller.on_exit()
        QGuiApplication.exit(0)

    def recompile_interfaces(self):
        interfaces = ['thumb_viewer_ui', 'full_view_base_ui', 'scroll_bar_widget_ui', 'favorite_line_ui', 'tool_box_ui',
                      'fav_change_dialog_ui', 'video_player_widget', 'playlist_ui', 'dialog_base_ui', 'setting_ui']
        base_dir = 'E:/Dropbox/Hobby/PRG/PyWork/FGet'
        source_dir = base_dir + '/view/ui/'
        dest_dir = base_dir + '/view/qt_ui/'

        pyuic5 = 'C:/Python34/Lib/site-packages/PyQt5/pyuic5.bat '

        for fname in interfaces:
            source = source_dir + fname + '.ui'
            dest = dest_dir + fname + '.py'
            command = pyuic5 + source + ' -o ' + dest
            print(command)
            os.system(command)
