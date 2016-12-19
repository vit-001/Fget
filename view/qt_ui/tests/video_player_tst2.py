__author__ = 'Vit'
# !/usr/bin/env python

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QWidget)


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        fileName = "E:/Dropbox/Hobby/PRG/PyWork/FGet/view/qt_ui/files/1.mp4"
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

        self.mediaPlayer.play()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    player = VideoPlayer()
    player.resize(320, 240)
    player.show()

    sys.exit(app.exec_())
