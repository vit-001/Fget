__author__ = 'Nikitin'

import os

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtGui import QPixmap, QIcon

from view.qt_ui.playlist_tst_ui import Ui_Playlist

from view.qt_widget.qt_dialog_base import DialogBase

from base_classes import AbstractPlaylistView,ControllerFromViewInterface
from setting import Setting
from playlist import PlaylistEntry

class QTPlaylistView(QMainWindow,AbstractPlaylistView):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)#, parent,QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        Setting.desktop=QApplication.desktop().screenGeometry()
        self.ui=Ui_Playlist()

        savecwd=os.getcwd()
        os.chdir('../../ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.ui.statusbar.hide()

        self.setGeometry(Setting.playlist_geometry())

        self.binding()
        # self.load_playlist()

        self.small=False
        self.ui.bn_size.setIcon(QIcon(QPixmap('../../qt_ui/files/icons/basic-application/minimize3.png')))
        # self.set_small_view(self.small)

    def binding(self):
        # self.ui.bn_play.clicked.connect(self.on_play_clicked)
        # self.ui.bn_add_from_fav.clicked.connect(self.on_fav_add_clicked)
        # self.ui.bn_next.clicked.connect(self.on_next_clicked)
        # self.ui.bn_prev.clicked.connect(self.on_prev_clicked)
        self.ui.bn_size.clicked.connect(self.toggle_small_view)


    # def load_playlist(self):
    #     for item in self.playlist.list:
    #         self.ui.playlist.addItem(item.url.to_save())
    #     self.ui.playlist.setCurrentRow(self.playlist.current_index)

    # def index_changed(self,index):
    #     self.ui.playlist.setCurrentRow(index)
    #     if self.player.state()!=QMediaPlayer.StoppedState:
    #         self.controller.goto_url(self.playlist.current_entry.url)

    # def on_play_clicked(self):
    #     # print('play')
    #     self.playlist.current_index=self.ui.playlist.currentRow()
    #     self.controller.goto_url(self.playlist.current_entry.url)
    #     # self.playlist.next()

    # def on_next_clicked(self):
    #     self.playlist.next()
    #
    # def on_prev_clicked(self):
    #     self.playlist.prev()


    # def on_fav_add_clicked(self):
    #     items=self.controller.get_favorites().get_categories()
    #
    #     item, ok = QInputDialog.getItem(self, '',"Add from group", items, 0, False,QtCore.Qt.Popup)
    #     if ok and item:
    #         fav_list = self.controller.get_favorites().get(item)
    #         for i in fav_list:
    #             if i.is_video():
    #                 self.playlist.add(PlaylistEntry(i.url))
    #         self.ui.playlist.clear()
    #         self.load_playlist()

    def toggle_small_view(self):
        self.small = not self.small
        self.set_small_view(self.small)

    def set_small_view(self,small=True):
        if small:
            self.ui.mid_frame.hide()
            self.ui.top_frame.hide()
            self.up
            self.ui.bn_size.setIcon(QIcon(QPixmap('../../qt_ui/files/icons/basic-application/maximize.png')))
            self.saved_geometry=self.saveGeometry()
            self.setGeometry(100,100,0,0)
            # self.resize(0,0)
            self.setWindowOpacity(1)
            # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.ui.mid_frame.show()
            self.ui.top_frame.show()
            self.ui.bn_size.setIcon(QIcon(QPixmap('../../qt_ui/files/icons/basic-application/minimize3.png')))
            self.restoreGeometry(self.saved_geometry)
            self.setWindowOpacity(1)
            # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
            self.show()

        # self.setGeometry(Setting.playlist_geometry(small))



import os

class InterfaceCompiler():
    def __init__(self,test_compile=False):

        self.test_compile=test_compile

        self.interfaces=['playlist_tst_ui']

        self.test_interfaces=[]

        if self.test_compile:
            self.interfaces.extend(self.test_interfaces)

        self.base_dir='E:/Dropbox/Hobby/PRG/PyWork/FGet'
        self.source_dir=self.base_dir+'/view/ui/'
        self.dest_dir=self.base_dir+'/view/qt_ui/'

        self.pyuic5='C:/Python34/Lib/site-packages/PyQt5/pyuic5.bat '


    def compile_interfaces(self):

        for fname in self.interfaces:
            source=self.source_dir+fname+'.ui'
            dest=self.dest_dir+fname+'.py'
            command=self.pyuic5+source+' -o '+dest
            print(command)
            os.system(command)

    def run_all(self):
        for fname in self.interfaces:
            os.system('C:/Python34/pythonw '+self.dest_dir+'tests/'+fname+'_tst.py')


if __name__ == "__main__":
    ic=InterfaceCompiler()
    ic.compile_interfaces()

    import sys
    app = QApplication(sys.argv)
    myapp = QTPlaylistView()
    myapp.show()
    sys.exit(app.exec_())