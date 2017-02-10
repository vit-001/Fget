__author__ = 'Nikitin'

import sys

from view.qt_ui.full_view_ui import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_full_view()
        self.ui.setupUi(self)
        self.resize(800, 800)

        # l_rect=self.contentsRect()

        self.pix = QtGui.QPixmap("../files/photo.jpg")
        # p_rect=self.pix.rect()

        # if l_rect.height()/l_rect.width()<p_rect.height()/p_rect.width():
        #     pix1=self.pix.scaledToHeight(l_rect.height())
        # else:
        #     pix1=self.pix.scaledToWidth(l_rect.width())
        #
        # print(pix1.rect())


        self.pixLabel = QtWidgets.QLabel(self)
        # self.pixLabel.setGeometry(self.contentsRect())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixLabel.sizePolicy().hasHeightForWidth())
        self.pixLabel.setSizePolicy(sizePolicy)
        self.pixLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.pixLabel.setText("")
        # self.pixLabel.setPixmap(pix1)
        self.pixLabel.setScaledContents(False)
        self.pixLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.pixLabel.setObjectName("pixLabel")

        self._redraw()

    def resizeEvent(self, *args, **kwargs):
        self._redraw()

    def _redraw(self):
        l_rect = self.contentsRect()
        p_rect = self.pix.rect()

        if l_rect.height() / l_rect.width() < p_rect.height() / p_rect.width():
            pix1 = self.pix.scaledToHeight(l_rect.height())
        else:
            pix1 = self.pix.scaledToWidth(l_rect.width())

        self.pixLabel.setGeometry(l_rect)
        self.pixLabel.setPixmap(pix1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
