__author__ = 'Vit'

from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from base_classes import (ControllerFromViewInterface, AbstractThumbView, URL, AbstractViewManager)
from setting import Setting

from view.qt_ui.thumb_viewer_ui import Ui_MainWindow

from view.qt_widget.qt_progress_line import QProgressHLine
from view.qt_widget.qt_button_line import QButtonLine
from view.qt_widget.qt_thumb_view import QThumbViewVS

from history import History, HistoryRecord, HistoryException


class QTThumbViewer(QMainWindow, AbstractThumbView):
    def __init__(self, parent=None, Qt_WindowFlags_flags=0, view_manager=AbstractViewManager):
        QMainWindow.__init__(self, parent)
        self.manager=view_manager
        self.controller = view_manager.get_controller()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.url = None
        self.history=History(self.on_history_changed)
        self.back_page=None

        self.make_widget()

    def make_widget(self):
        self.pl = QProgressHLine(self.ui.bottom_frame, height=4)
        self.pl.new_progress('blue', QtCore.Qt.blue)
        self.ui.bottom_frame_layout.addWidget(self.pl)
        self.pl.hide()

        self.controls = QButtonLine(self.ui.bottom_frame)
        self.ui.bottom_frame_layout.addWidget(self.controls)
        self.controls.hide()

        self.pages = QButtonLine(self.ui.bottom_frame)
        self.ui.bottom_frame_layout.addWidget(self.pages)
        self.pages.hide()

        self.sites = QButtonLine(self.ui.top_frame)
        self.ui.top_frame_layout.addWidget(self.sites)
        self.sites.hide()

        self.nested_sites = QButtonLine(self.ui.top_frame)
        self.ui.top_frame_layout.addWidget(self.nested_sites)
        self.nested_sites.hide()

        self.thumbs = QThumbViewVS(self.ui.mid_frame)
        self.ui.mid_frame_layout.addWidget(self.thumbs)

        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thumbs.sizePolicy().hasHeightForWidth())
        self.thumbs.setSizePolicy(sizePolicy)

        #Binding
        self.ui.bn_back.clicked.connect(self.go_back)
        self.ui.bn_go.clicked.connect(lambda:self.controller.goto_url(URL(self.ui.combo_history.currentText())))
        self.ui.bn_playlist.clicked.connect(self.manager.toggle_playlist_view)
        self.ui.bn_toolbox.clicked.connect(self.manager.toggle_tool_view)

    def panic(self):
        self.showMinimized()

    def add_site_button(self, text='', action=lambda: 0,menu_items=None,tooltip=''):
        self.add_button_with_menu(self.sites,text,action,menu_items,tooltip)

    def add_site_nested(self, text='', action=lambda: 0, menu_items=dict(),tooltip=''):
        self.add_button_with_menu(self.nested_sites,text,action,menu_items,tooltip)

    def add_control(self, text='', action=lambda: 0,menu_items=None,tooltip=''):
        self.add_button_with_menu(self.controls,text,action,menu_items,tooltip)

    def add_page(self, text='', action=lambda: 0,menu_items=None,tooltip=''):
        self.add_button_with_menu(self.pages,text,action,menu_items,tooltip)

    def add_button_with_menu(self,button_line, text='', action=lambda: 0,menu_items=None,tooltip=''):
        if menu_items is not None:
            menu = QMenu(self)
            for key in sorted(menu_items):
                menu_action=QAction(key, self, triggered=menu_items[key])
                menu.addAction(menu_action)
        else:
            menu=None
        button_line.add_button(text, action, menu, tooltip)

    def add_preview(self, picture_fname='', action=lambda: 0, popup_text=''):
        self.thumbs.add(picture_fname, action, popup_text)
        self.setWindowTitle(self.url.get() + ' (' + str(self.thumbs.count) + ' thumbs)')
        QtCore.QEventLoop().processEvents(QtCore.QEventLoop.AllEvents)
        self.update()

    def set_cycle_handler(self, handler=lambda: 0):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(handler)
        self.timer.start(100)

    def prepare(self, url=URL()):
        context=None
        if self.back_page is None or self.back_page.data!=url:
            if self.url is not None:
                self.history.put(HistoryRecord(self.url,self.thumbs.context))
        else:
            context=self.back_page.context
        self.thumbs.clear()
        self.pages.clear()
        self.controls.clear()
        self.nested_sites.clear()
        self.url = url
        self.setWindowTitle(url.get())
        self.ui.combo_history.insertItem(0,self.url.to_save())
        self.ui.combo_history.setCurrentIndex(0)
        self.update()

        self.thumbs.context=context
        self.back_page=None

    def go_back(self):
        try:
            self.back_page=self.history.pop()
            self.controller.goto_url(self.back_page.data)
        except HistoryException:
            pass

    def on_history_changed(self):
        self.ui.combo_history.clear()
        for item in self.history.get_last_data(20):
            self.ui.combo_history.insertItem(0,item.to_save())

    def get_url(self):
        return self.url

    def progress_stop(self):
        self.pl.set_value('blue', 0)
        self.pl.hide()

    def progress_set(self, value):
        self.pl.set_value('blue', value)

    def progress_init(self, maximum=100):
        self.pl.set_max(maximum)
        self.pl.show()

    def show_status(self, txt=''):
        self.ui.statusbar.showMessage(txt,3000)

    def closeEvent(self, *args, **kwargs):
        self.manager.on_close_event()
