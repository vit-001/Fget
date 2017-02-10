__author__ = 'Nikitin'

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow)

from view.qt_ui.video_player import *


class MyWin(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_VideoPlayer()
        self.ui.setupUi(self)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player_widget = QVideoWidget(self.ui.mid_frame)
        self.ui.mid_frame_layout.addWidget(self.media_player_widget)

        self.media_player.setVideoOutput(self.media_player_widget)
        self.media_player.error.connect(self.handleError)

        # fileName="E:/Dropbox/Hobby/PRG/PyWork/FGet/view/qt_ui/files/1.mp4"
        # self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

        # fileName="E:/exchange/DiskD/kl/1/road_to_abbi_big-1080.mp4.Epidemz.net_Triksa.com.mp4"
        # self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))



        self.ui.bn_go.clicked.connect(self.go)

        self.media_player.bufferStatusChanged.connect(self.buf)
        self.media_player.mediaStatusChanged.connect(self.med)

        # url='http://tubedupe.com/get_file/1/693b07616d5019e3e266e772676e3048/56000/56102/56102.mp4'
        url = 'http://tubedupe.com/get_file/1/4b274e3f4027b13bf6d6ae5601dd7a09/50000/50768/50768.mp4'
        url = 'http://www.mypornovideo.net/video_file/2015/2/830/grudastaja_blondinka_ebetsja_s_kuchejj_muzhikov.flv'
        url = "http://im.50f9bc00.493dea4.cdn2b.movies.mxn.com/0/399/399060/NOWATERMARK_IPOD.mp4?s=1423689551&e=1423696751&ri=1227&rs=44&h=d0a58a04acc858983a202b5e8dea575a"

        self.media_player.setMedia(QMediaContent(QUrl(url)))

        self.media_player.play()
        self.media_player.setMuted(True)
        print(self.media_player.duration())

        print('Done')

    def handleError(self):
        print('Error: ' + self.media_player.errorString())

    def buf(self, percent):
        print(percent, '%')

    def med(self, media):
        print(media)

    def go(self):
        dur = self.media_player.duration()
        pos = self.media_player.position()

        print(dur // 1000, pos // 1000)
        print(self.media_player.bufferStatus())

        # self.hide()
        self.media_player.stop()

        # self.media_player.setPosition(dur*98//100)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
