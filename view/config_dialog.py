__author__ = 'Nikitin'

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from base_classes import AbstractViewManager

from setting import Setting
from view.qt_ui.setting_ui import Ui_ConfigDialog


class ConfigDialog(QDialog):
    def __init__(self, parent=None, manager=AbstractViewManager):
        QDialog.__init__(self, parent)
        if Setting.view_debug: print('Config dialog: init')

        self.manager = manager

        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)

        self.load_setting()
        self.binding()


    def load_setting(self):
        self.ui.chk_controller_debug.setChecked(Setting.controller_debug)
        self.ui.chk_view_debug.setChecked(Setting.view_debug)
        self.ui.chk_model_debug.setChecked(Setting.model_debug)
        self.ui.chk_site_debug.setChecked(Setting.site_debug)
        self.ui.chk_fav_debug.setChecked(Setting.fav_debug)

        self.ui.chk_statistic.setChecked(Setting.statistic)
        self.ui.chk_video_info.setChecked(Setting.video_info)

        self.ui.input_base_folder.setText(Setting.base_dir)
        self.ui.input_fav_file.setText(Setting.fav_filename)
        self.ui.input_playlist_file.setText(Setting.playlist_filename)
        self.ui.input_dest_folder.setText(Setting.download_dir)
        self.ui.input_uget_folder.setText(Setting.uget_path)

        self.ui.input_exchange_folder.setText(Setting.exchange_path)

        self.ui.chk_download_simultaneously.setChecked(Setting.download_simultaneously)

        if Setting.download_method=='uget':
            self.ui.radio_use_uget.setChecked(True)
        elif Setting.download_method=='server':
            self.ui.radio_use_dropbox.setChecked(True)

    def binding(self):

        self.ui.bn_dest_folder.clicked.connect(lambda: self.ui.input_dest_folder.setText(
            QFileDialog.getExistingDirectory(self, 'Load files to..', self.ui.input_dest_folder.text())))

        self.ui.bn_base_folder.clicked.connect(lambda: self.ui.input_base_folder.setText(
            QFileDialog.getExistingDirectory(self, 'Temp files base folder', self.ui.input_base_folder.text())))

        self.ui.bn_uget_folder.clicked.connect(lambda: self.ui.input_uget_folder.setText(
            QFileDialog.getExistingDirectory(self, 'uGet folder', self.ui.input_uget_folder.text())))

        self.ui.bn_fav_file.clicked.connect(lambda: self.ui.input_fav_file.setText(
            QFileDialog.getSaveFileName(self, 'Save favorites to', self.ui.input_fav_file.text(),
                                        'Favorites files (*.fav)')[0]))

        self.ui.bn_playlist_file.clicked.connect(lambda: self.ui.input_playlist_file.setText(
            QFileDialog.getSaveFileName(self, 'Save playlist to', self.ui.input_playlist_file.text(),
                                        'Playlist files (*.pl)')[0]))

        self.ui.bn_exchange_folder.clicked.connect(lambda: self.ui.input_exchange_folder.setText(
            QFileDialog.getExistingDirectory(self, 'Server exchange folder', self.ui.input_exchange_folder.text())))


        self.ui.bn_recompile.clicked.connect(self.manager.recompile_interfaces)
        self.ui.bn_download_now.clicked.connect(self.manager.get_controller().download_now)

    def save_setting(self):
        Setting.controller_debug = self.ui.chk_controller_debug.isChecked()
        Setting.view_debug = self.ui.chk_view_debug.isChecked()
        Setting.model_debug = self.ui.chk_model_debug.isChecked()
        Setting.site_debug = self.ui.chk_site_debug.isChecked()
        Setting.fav_debug = self.ui.chk_fav_debug.isChecked()

        Setting.statistic = self.ui.chk_statistic.isChecked()
        Setting.video_info = self.ui.chk_video_info.isChecked()

        Setting.fav_filename=self.ui.input_fav_file.text()
        Setting.playlist_filename=self.ui.input_playlist_file.text()
        Setting.base_dir=self.ui.input_base_folder.text().rstrip('/')+'/'
        Setting.download_dir=self.ui.input_dest_folder.text().rstrip('/')+'/'
        Setting.uget_path=self.ui.input_uget_folder.text().rstrip('/')+'/'
        Setting.exchange_path=self.ui.input_exchange_folder.text().rstrip('/')+'/'

        Setting.download_simultaneously=self.ui.chk_download_simultaneously.isChecked()

        if self.ui.radio_use_uget.isChecked():
            Setting.download_method="uget"
        elif self.ui.radio_use_dropbox.isChecked():
            Setting.download_method='server'

    def accept(self):
        if Setting.view_debug: print('ConfigDialog: Accept')
        self.save_setting()
        super().accept()



