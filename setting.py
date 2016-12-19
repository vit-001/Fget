__author__ = 'Vit'

from PyQt5 import QtCore


class Setting():
    desktop = None

    model_debug = False
    site_debug = False
    controller_debug = True
    view_debug = True
    fav_debug = True

    statistic = True
    video_info = True

    show_sites = False

    fav_filename = 'files/favorites.fav'
    fav_tmp_filename = 'files/favorites.fav.tmp'

    playlist_filename = 'files/playlist.pl'

    base_dir = 'e:/out/'

    download_dir = 'e:/out/down/'
    uget_path = 'E:/Dropbox/Hobby/PRG/soft/uGet/bin/'
    exchange_path = 'E:/Dropbox/Public/tmp/'

    download_method = 'uget'
    download_simultaneously = True

    setting_file = 'files/setting.cfg'

    @staticmethod
    def rect(x, y, w, h):
        return QtCore.QRect(Setting.desktop.width() * x // 100, Setting.desktop.height() * y // 100,
                            Setting.desktop.width() * w // 100, Setting.desktop.height() * h // 100)

    @staticmethod
    def thumb_view_geometry():
        return Setting.rect(2, 5, 23, 80)

    @staticmethod
    def full_view_geometry():
        return Setting.rect(27, 5, 70, 90)

    @staticmethod
    def tool_box_geometry():
        return Setting.rect(2, 89, 23, 0)

    @staticmethod
    def fav_change_dialog_geometry():
        return Setting.rect(5, 70, 25, 0)

    @staticmethod
    def playlist_geometry(small=False):
        if small:
            return Setting.rect(1, 8, 0, 0)
        else:
            return Setting.rect(1, 8, 23, 50)

    @staticmethod
    def uget():
        return Setting.uget_path + 'uget'

    @staticmethod
    def load_setting(file):
        for line in file:
            exec(line)

    @staticmethod
    def save_setting(file):
        print('saving setting')
        file.write('Setting.model_debug=' + str(Setting.model_debug) + '\n')
        file.write('Setting.site_debug=' + str(Setting.site_debug) + '\n')
        file.write('Setting.controller_debug=' + str(Setting.controller_debug) + '\n')
        file.write('Setting.view_debug=' + str(Setting.view_debug) + '\n')
        file.write('Setting.fav_debug=' + str(Setting.fav_debug) + '\n')

        file.write('Setting.statistic=' + str(Setting.statistic) + '\n')
        file.write('Setting.video_info=' + str(Setting.video_info) + '\n')

        file.write('Setting.fav_filename="' + str(Setting.fav_filename) + '"\n')
        file.write('Setting.playlist_filename="' + str(Setting.playlist_filename) + '"\n')

        file.write('Setting.base_dir="' + str(Setting.base_dir) + '"\n')
        file.write('Setting.download_dir="' + str(Setting.download_dir) + '"\n')
        file.write('Setting.uget_path="' + str(Setting.uget_path) + '"\n')

        file.write('Setting.exchange_path="' + str(Setting.exchange_path) + '"\n')
        file.write('Setting.download_method="' + str(Setting.download_method) + '"\n')

        file.write('Setting.download_simultaneously=' + str(Setting.download_simultaneously) + '\n')
