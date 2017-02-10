__author__ = 'Nikitin'

import os

from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import *

from base_classes import AbstractPlaylistView, AbstractViewManager
from playlist import PlaylistEntry, PlaylistException
from view.qt_ui.playlist_ui import Ui_Playlist


class QTPlaylistView(QMainWindow, AbstractPlaylistView):
    def __init__(self, parent=None, Qt_WindowFlags_flags=0, view_manager=AbstractViewManager(), player=None):
        QMainWindow.__init__(self, parent, Qt_WindowFlags_flags)
        self.manager = view_manager
        self.controller = view_manager.get_controller()
        self.player = player
        self.playlist = self.controller.get_playlist()
        self.playlist.add_listeners(on_change_listener=self.load_playlist,
                                    on_change_index_listener=self.index_changed)

        self.ui = Ui_Playlist()

        savecwd = os.getcwd()
        os.chdir('view/ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.ui.statusbar.hide()

        self.binding()
        self.load_playlist()

    def binding(self):
        self.ui.bn_play.clicked.connect(self.on_play_clicked)
        self.ui.bn_add_from_fav.clicked.connect(self.on_fav_add_clicked)
        self.ui.bn_next.clicked.connect(self.on_next_clicked)
        self.ui.bn_prev.clicked.connect(self.on_prev_clicked)
        self.ui.bn_save.clicked.connect(self.save_playlist)
        self.ui.bn_open.clicked.connect(self.open_playlist)
        self.ui.bn_delete.clicked.connect(self.on_delete_pressed)

    def load_playlist(self):
        self.ui.playlist.clear()
        for item in self.playlist.list:
            self.ui.playlist.addItem(item.url.to_save())
        self.ui.playlist.setCurrentRow(self.playlist.current_index)

    def index_changed(self, index):
        self.ui.playlist.setCurrentRow(index)
        if self.player.state() != QMediaPlayer.StoppedState:
            try:
                self.controller.goto_url(self.playlist.current_entry.url)
            except PlaylistException:
                pass

    def on_play_clicked(self):
        # print('play')
        self.playlist.current_index = self.ui.playlist.currentRow()
        try:
            self.controller.goto_url(self.playlist.current_entry.url)
            self.manager.get_video_view().playlist_connect(goto_prev=self.on_prev_clicked,
                                                           goto_next=self.on_next_clicked)
        except PlaylistException:
            pass

    def on_next_clicked(self):
        self.playlist.next()

    def on_prev_clicked(self):
        self.playlist.prev()

    def on_fav_add_clicked(self):
        items = self.controller.get_favorites().get_categories()

        item, ok = QInputDialog.getItem(self, '', "Add from group", items, 0, False, QtCore.Qt.Popup)
        if ok and item:
            fav_list = self.controller.get_favorites().get(item)
            for i in fav_list:
                if i.is_video():
                    self.playlist.add(PlaylistEntry(i.url))

    def on_delete_pressed(self):
        indexes = self.ui.playlist.selectedIndexes()

        delete_list = list()
        for i in indexes:
            delete_list.append(i.row())

        self.playlist.delete_items(delete_list)

    def save_playlist(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save to', 'files/untitled', 'Playlist files (*.fget_pl)')
        if filename:
            file = open(filename, 'w')
            self.playlist.save(file)
            file.close()

    def open_playlist(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open playlist', 'files/', 'Playlist files (*.fget_pl)')

        if filename:
            file = open(filename)
            self.playlist.open(file)
