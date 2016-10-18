__author__ = 'Nikitin'

import sys

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)

from view.qt_ui.video_player import *

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_VideoPlayer()
        self.ui.setupUi(self)

        self.mediaPlayer = QMediaPlayer()
        videoWidget = QVideoWidget(self.ui.mid_frame)

        self.ui.mid_frame_layout.addWidget(videoWidget)

        self.mediaPlayer.setVideoOutput(videoWidget)

        file=QUrl.fromLocalFile('E:/Dropbox/Hobby/PRG/PyWork/FGet/view/qt_ui/files/1.mp4')
        print(file)

        self.mediaPlayer.setMedia(QMediaContent(file))

        self.mediaPlayer.play()

        # openButton = QPushButton("Open...")
        # openButton.clicked.connect(self.openFile)
        #
        # self.playButton = QPushButton()
        # self.playButton.setEnabled(False)
        # self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # self.playButton.clicked.connect(self.play)
        #
        # self.positionSlider = QSlider(Qt.Horizontal)
        # self.positionSlider.setRange(0, 0)
        # self.positionSlider.sliderMoved.connect(self.setPosition)
        #
        # self.errorLabel = QLabel()
        # self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
        #         QSizePolicy.Maximum)
        #
        # controlLayout = QHBoxLayout()
        # controlLayout.setContentsMargins(0, 0, 0, 0)
        # controlLayout.addWidget(openButton)
        # controlLayout.addWidget(self.playButton)
        # controlLayout.addWidget(self.positionSlider)
        #
        # layout = QVBoxLayout()
        # layout.addWidget(videoWidget)
        # layout.addLayout(controlLayout)
        # layout.addWidget(self.errorLabel)
        #
        # self.setLayout(layout)
        #
        # self.mediaPlayer.setVideoOutput(videoWidget)
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        # self.mediaPlayer.positionChanged.connect(self.positionChanged)
        # self.mediaPlayer.durationChanged.connect(self.durationChanged)
        # self.mediaPlayer.error.connect(self.handleError)


        #
        # self.pixmap=QtGui.QPixmap("E:/Dropbox/Hobby/PRG/PyWork/FGet/files/photo.jpg")
        #
        # self.toolButton = QtWidgets.QToolButton(self.ui.mid_frame)
        # icon = QtGui.QIcon()
        # icon.addPixmap(self.pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.toolButton.setIcon(icon)
        # self.toolButton.setIconSize(QtCore.QSize(200, 200))
        # self.toolButton.setObjectName("toolButton")
        # self.ui.mid_frame_layout.addWidget(self.toolButton)
        # self.toolButton.setText("...")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
