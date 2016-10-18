__author__ = 'Nikitin'

import os

class InterfaceCompiler():
    def __init__(self,test_compile=False):

        self.test_compile=test_compile

        self.interfaces=['thumb_viewer_ui','full_view_base_ui','scroll_bar_widget_ui','favorite_line_ui','tool_box_ui',
                         'fav_change_dialog_ui','video_player_widget','playlist_ui','dialog_base_ui','setting_ui']

        self.test_interfaces=['tst_qpixmap','tst','video_player']

        if self.test_compile:
            self.interfaces.extend(self.test_interfaces)

        self.base_dir='E:/Dropbox/Hobby/PRG/PyWork/FGet'
        self.source_dir=self.base_dir+'/view/ui/'
        self.dest_dir=self.base_dir+'/view/qt_ui/'

        self.pyuic5='C:/Python34/Lib/site-packages/PyQt5/pyuic5.bat '


    def compile_interfaces(self):

        for fname in self.interfaces:
            source=self.source_dir+fname+'.ui'
            dest=self.dest_dir+fname+'.py'
            command=self.pyuic5+source+' -o '+dest
            print(command)
            os.system(command)

    def run_all(self):
        for fname in self.interfaces:
            os.system('C:/Python34/pythonw '+self.dest_dir+'tests/'+fname+'_tst.py')


if __name__ == "__main__":
    ic=InterfaceCompiler(True)
    ic.compile_interfaces()
    ic.run_all()

