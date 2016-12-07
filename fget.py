__author__ = 'Nikitin'


if __name__ == "__main__":

    from model import SiteVewerModel
    import sys

    from view.view_manager import QTViewManager
    from controller import Controller
    from setting import Setting

    setting_file=Setting.setting_file #default config

    for item in sys.argv[1:]:
        if item.startswith('-setting='):
            setting_file=item.partition('=')[2]
            Setting.setting_file=setting_file
        elif item.startswith('-info'):
            Setting.show_sites=True
        else:
            print('Unknown argument:',item,', ignoring')

    try:
        file=open(setting_file)
        Setting.load_setting(file)
        file.close()
    except OSError:
        print('Setting file not found, use default setting')

    # import os
    # os.spawnl(os.P_DETACH, Setting.uget_path+'uget.exe','-gtk')

    print('Todo:')
    print('')
    print('Thats all')
    print('')
    print('https://www.veronicca.com/', 'verifyed, simple, good')
    print('http://porndoe.com/', 'verifyed, simple, bad')
    print('http://www.gotporn.com/', 'verifyed')
    print('http://ru.tubepornclassic.com/', 'verifyed, retro')#
    print("Let's go..")


    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    controller=Controller(QTViewManager,SiteVewerModel)
    sys.exit(app.exec_())
