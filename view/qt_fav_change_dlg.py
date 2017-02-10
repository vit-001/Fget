from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from setting import Setting
from view.qt_ui.fav_change_dialog_ui import Ui_EditDialog

__author__ = 'Vit'


class FavoriteChangeDialog(QDialog):
    def __init__(self, parent=None, record=None, favorites=None):
        QDialog.__init__(self, parent)

        self.favorites = favorites
        self.record = record

        self.ui = Ui_EditDialog()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(Setting.fav_change_dialog_geometry())

        if record.is_thumb():
            self.ui.input_type.setText('Thumbnail page')
        elif record.is_pix():
            self.ui.input_type.setText('Pictures page')
        elif record.is_video():
            self.ui.input_type.setText('Video page')
        else:
            self.ui.input_type.setText('Unknown page')

        if record.name != '':
            self.ui.input_name.setText(self.record.name)
        else:
            self.ui.input_name.setText(self.record.url.get())

        self.ui.input_url.setText(self.record.url.get())

        self.ui.combo_category.addItems(self.favorites.get_categories())
        self.ui.combo_category.setCurrentText(record.category)

        self.ui.check_delete.stateChanged.connect(self.check_state_changed)

    def check_state_changed(self):
        if self.ui.check_delete.isChecked():
            self.ui.combo_category.setDisabled(True)
            self.ui.input_name.setDisabled(True)
        else:
            self.ui.combo_category.setDisabled(False)
            self.ui.input_name.setDisabled(False)

    def accept(self):
        if Setting.view_debug: print('FavoriteChangeDialog: Accept')

        if self.ui.check_delete.isChecked():
            if Setting.view_debug: print(' deleting')
            self.favorites.delete(self.record)

        else:
            new_category = self.ui.combo_category.currentText().strip().replace(' ', '_')
            if new_category != self.record.category:
                if Setting.view_debug: print(' moving to',
                                             self.ui.combo_category.currentText().strip().replace(' ', '_'))
                self.favorites.delete(self.record, True)
                self.record.category = new_category
            if Setting.view_debug: print(' renaming to', self.ui.input_name.text())
            self.record.name = self.ui.input_name.text().strip().replace(' ', '_')

            self.favorites.add(self.record)

            # self.favorites.changed(self.record)

        super().accept()
