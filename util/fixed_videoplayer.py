#!/usr/bin/env python

from PyQt5.QtCore import QDir, Qt, QUrl, QUrlQuery
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)


class VideoPlayer(QWidget):

    def __init__(self, parent=None, url=None):
        super(VideoPlayer, self).__init__(parent)

        self.url=url

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        openButton = QPushButton("Open...")
        openButton.clicked.connect(self.openFile)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        # fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
        #         QDir.homePath())
        #
        # print(fileName)



        if self.url is not None:

            self.mediaPlayer.setMedia(QMediaContent(q_url))
            self.playButton.setEnabled(True)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    url='https://redirector.googlevideo.com/videoplayback?requiressl=yes&id=d7186d1009d68503&itag=22&source=webdrive&ttl=transient&app=explorer&ip=2604:a880:800:10::188e:f001&ipbits=32&expire=1481242230&sparams=requiressl,id,itag,source,ttl,ip,ipbits,expire&signature=A4D38F48A008E8759441DE3722E7FA7829C4F84.79C6FCF150C2F329DDCE6CA138529EFD81374B94&key=ck2&mm=31&mn=sn-ab5l6n7y&ms=au&mt=1481227650&mv=m&nh=IgpwcjAzLmxnYTA3KhIyNjA0OmE4ODA6ODAwOjoxMDA&pl=48&title=cloudspro.net'

    q_url = QUrl(url)

    player = VideoPlayer(url=q_url)
    player.resize(320, 240)
    player.show()

    sys.exit(app.exec_())
