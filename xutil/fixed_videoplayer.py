#!/usr/bin/env python

from PyQt5.QtCore import Qt, QUrl, QVariant
from PyQt5.QtNetwork import QNetworkProxy, QNetworkRequest, QNetworkCookie
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)


class VideoPlayer(QWidget):
    def __init__(self, parent=None, url=None):
        super(VideoPlayer, self).__init__(parent)

        self.url = url

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


            request=QNetworkRequest(q_url)
            # coockies = {'_gat': '1', 'protect': 'BPJvGkuwOdy0D4amF44YTA', '_ga': 'GA1.2.638382635.1487974825'}


            # nc=[
            #     QNetworkCookie('_gat'.encode(),'1'.encode()),
            #     QNetworkCookie('protect'.encode(), 'BPJvGkuwOdy0D4amF44YTA'.encode()),
            #     QNetworkCookie('_ga'.encode(), 'GA1.2.638382635.1487974825'.encode())
            #     ]


            # request.setHeader(QNetworkRequest.CookieHeader,nc)



            # proxy=QNetworkProxy()
            # proxy.setType(QNetworkProxy.HttpProxy)
            # proxy.setHostName("proxy.antizapret.prostovpn.org")
            # proxy.setPort(3128)
            #
            # proxy.setApplicationProxy(proxy)

            # QNetworkProxy.setApplicationProxy(proxy)


            self.mediaPlayer.setMedia(QMediaContent(request))
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

    url = 'https://cluster8b.heavy-r.com/v/05689c5250aed81763a50ffe1baa5d71/58ca8dac/vid/0a/04/a4/0a04a4cf943928d.mp4'
    url2= 'http://media.collectionofbestporn.com:8080/videos/5/8/a/6/b/58a6b3d600d8a.mp4'
    url3='http://cdn4.videos.motherlessmedia.com/videos/E5C4682.mp4?fs=opencloud'

    q_url = QUrl(url)

    player = VideoPlayer(url=q_url)
    player.resize(320, 240)
    player.show()

    sys.exit(app.exec_())
