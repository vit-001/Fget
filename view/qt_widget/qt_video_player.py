__author__ = 'Vit'

__all__ = ['QThumbViewVS']

import sys, os

from urllib.parse import urlparse

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtWidgets import (QApplication, QFileDialog, QAction, QMenu,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QMainWindow)

from view.qt_ui.video_player_widget import Ui_VideoPlayer


class VideoPlayer(QWidget):
    def __init__(self, parent=None, mute=True):
        QWidget.__init__(self, parent)

        self.ui = Ui_VideoPlayer()

        savecwd = os.getcwd()
        os.chdir('view/ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.ui.bn_size.hide()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # self.item=QGraphicsVideoItem()
        # self.ui.mid_frame_grid_layout.addItem(self.item,0,0)
        # self.media_player.setVideoOutput(self.item)

        self.media_player_widget = QVideoWidget(self.ui.mid_frame)
        self.ui.mid_frame_grid_layout.addWidget(self.media_player_widget, 0, 0)
        self.media_player.setVideoOutput(self.media_player_widget)


        # self.media_player.stateChanged.connect(self.state_changed)
        self.media_player.bufferStatusChanged.connect(self.buffer_status_changed)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.error.connect(self.handleError)
        # self.media_player.metaDataChanged.connect(self.meta_data_changed)

        self.ui.bn_mute.setChecked(mute)
        self.mute()
        self.connect_to_playlist(connected=False, toggle_playlist=lambda: None)
        self.ui.dial_volume.setFixedWidth(50)

        # binding
        self.ui.bn_play.clicked.connect(self.media_player.play)
        self.ui.bn_pause.clicked.connect(self.media_player.pause)
        self.ui.bn_mute.clicked.connect(self.mute)
        self.ui.bn_stop.clicked.connect(self.media_player.stop)
        self.ui.bn_next.clicked.connect(self.next)
        self.ui.bn_prev.clicked.connect(self.prev)
        self.ui.bn_playlist.clicked.connect(self.show_playlist)
        self.ui.bn_uget.clicked.connect(self.on_uget_pressed)

        self.ui.progress_slider.sliderMoved.connect(self.media_player.setPosition)
        # self.ui.spin_volume.valueChanged.connect(self.media_player.setVolume)
        self.ui.dial_volume.valueChanged.connect(self.media_player.setVolume)

        self.url = ''
        self.altermate = list()
        self.duration = '0:00'
        self.change_position = None
        self.uget_handler = lambda fname='', url='': None
        # self.on_end_of_playing=lambda :None

    def icons_set(self, bn, fname_off, fname_on=None):
        icon = QIcon()
        icon.addPixmap(QPixmap(fname_off), QIcon.Normal, QIcon.Off)
        if fname_on is not None:
            icon.addPixmap(QPixmap(fname_on), QIcon.Normal, QIcon.On)
        bn.setIcon(icon)

    def connect_to_playlist(self, connected=False, goto_prev=lambda: None, goto_next=lambda: None,
                            toggle_playlist=None):
        self.goto_next = goto_next
        self.goto_prev = goto_prev
        if toggle_playlist is not None:
            self.toggle_playlist = toggle_playlist
        self.connected = connected

        if self.connected:
            self.ui.playlist_frame.show()
            self.ui.bn_add.hide()
            self.ui.bn_minus.show()
        else:
            self.ui.playlist_frame.hide()
            self.ui.bn_add.show()
            self.ui.bn_minus.hide()

    def set_plus_handler(self, handler=lambda: None):
        self.ui.bn_add.clicked.connect(handler)

    def set_minus_handler(self, handler=lambda: None):
        self.ui.bn_minus.clicked.connect(handler)

    def set_uget_handler(self, handler=lambda fname='', url='': None):
        self.uget_handler = handler

    def on_uget_pressed(self, url=None):
        self.uget_handler(fname=urlparse(url.rstrip('/'))[2].rpartition('/')[2], url=url)

    def set_url(self, url=''):
        self.url = url
        self.altermate = list()
        self.ui.bn_size.hide()
        self.media_player.setMedia(QMediaContent(QUrl(url)))
        uget_menu = QMenu(self)
        uget_menu_action = QAction('Standart quality', self, triggered=self.get_handler(self.on_uget_pressed, url))
        uget_menu.addAction(uget_menu_action)
        self.ui.bn_uget.setMenu(uget_menu)

    def change_url(self, url):
        position = self.media_player.position()
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(QUrl(url)))
        self.media_player.play()
        self.change_position = position

    def add_alternate_url(self, caption='', url=''):
        self.ui.bn_size.show()
        self.altermate.append(dict(caption=caption, url=url))
        menu = QMenu(self)
        uget_menu = QMenu(self)
        for item in self.altermate:
            menu_action = QAction(item['caption'], self, triggered=self.get_handler(self.change_url, item['url']))
            menu.addAction(menu_action)
            uget_menu_action = QAction(item['caption'], self,
                                       triggered=self.get_handler(self.on_uget_pressed, item['url']))
            uget_menu.addAction(uget_menu_action)
        self.ui.bn_size.setMenu(menu)
        self.ui.bn_uget.setMenu(uget_menu)

    def get_handler(self, function, arg):
        return lambda: function(arg)

    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def next(self):
        self.goto_next()

    def prev(self):
        self.goto_prev()

    def show_playlist(self):
        self.toggle_playlist()

    def mute(self):
        if self.ui.bn_mute.isChecked():
            self.media_player.setMuted(True)
        else:
            self.media_player.setMuted(False)
            self.media_player.setVolume(self.ui.dial_volume.value())

    def little_forvard(self, s=30):
        self.media_player.setPosition(self.media_player.position() + s * 1000)

    def media_status_changed(self, status):
        # print('Media status=', status)

        if status == QMediaPlayer.StalledMedia:
            self.ui.progress_buffer.show()
        else:
            self.ui.progress_buffer.hide()

        if status == QMediaPlayer.BufferedMedia:
            if self.change_position is not None:
                # print('Changing position')
                self.media_player.setPosition(self.change_position)
                self.change_position = None
        if status == QMediaPlayer.EndOfMedia:
            self.goto_next()

    def buffer_status_changed(self, status):
        # print('Buffer status=', status)
        self.ui.progress_buffer.setValue(status)

    # def state_changed(self,status):
    #     print('State=', status)

    def state(self):
        return self.media_player.state()

    def positionChanged(self, position):
        self.ui.progress_slider.setValue(position)
        self.ui.lbl_time.setText(self.time_format(position) + ' / ' + self.duration)

    def durationChanged(self, duration):
        self.ui.progress_slider.setRange(0, duration)
        self.duration = self.time_format(duration)

    def time_format(self, ms):
        dur = ms // 1000
        minutes = dur // 60
        secundes = dur - minutes * 60
        return '%d:%02d' % (minutes, secundes)

    def handleError(self):
        print("Error in " + self.url + ': ' + self.media_player.errorString())


if __name__ == "__main__":
    fname = 'video_player_widget'

    base_dir = 'E:/Dropbox/Hobby/PRG/PyWork/FGet'
    source_dir = base_dir + '/view/ui/'
    dest_dir = base_dir + '/view/qt_ui/'

    pyuic5 = 'C:/Python34/Lib/site-packages/PyQt5/pyuic5.bat '

    source = source_dir + fname + '.ui'
    dest = dest_dir + fname + '.py'
    command = pyuic5 + source + ' -o ' + dest
    print(command)
    os.system(command)

    app = QApplication(sys.argv)
    myapp = VideoPlayer()
    myapp.show()

    url = 'http://tubedupe.com/get_file/1/4b274e3f4027b13bf6d6ae5601dd7a09/50000/50768/50768.mp4'
    url = 'http://tubedupe.com/get_file/1/bcf397405a4fda2e0e6998c498ce0edf/56000/56191/56191.mp4'
    myapp.set_url(url)

    sys.exit(app.exec_())
