from urllib.parse import urlparse

from base_classes import AbstractVideoView, AbstractViewManager, URL, MediaData
from favorites import FavoriteRecord
from playlist import PlaylistEntry, PlaylistException
from setting import Setting
from view.qt_full_view import FullView
from view.qt_widget.qt_video_player import VideoPlayer


class VideoView(FullView, AbstractVideoView):
    def __init__(self, parent=None, view_manager=AbstractViewManager):
        FullView.__init__(self, parent, view_manager)

        self.video_player = VideoPlayer(self.ui.mid_frame)
        self.ui.mid_frame_layout.addWidget(self.video_player)

        self.manager.add_keyboard_shortcut(self, 'Space', lambda: self.video_player.little_forvard(30))
        self.manager.add_keyboard_shortcut(self, 'Ctrl+Space', lambda: self.video_player.little_forvard(180))

        self.manager.add_keyboard_shortcut(self, 'PgUp', lambda: self.prev())
        self.manager.add_keyboard_shortcut(self, 'PgDown', lambda: self.next())

        self.video_player.connect_to_playlist(connected=False, toggle_playlist=self.manager.toggle_playlist_view)
        self.video_player.set_plus_handler(lambda: self.controller.get_playlist().add(PlaylistEntry(self.url)))
        self.video_player.set_minus_handler(self.delete_from_playlist)

        self.video_player.set_uget_handler(self.load_video)
        self.video_player.set_error_handler(self.on_error_handler)
        self.show()

        self.prev = lambda: None
        self.next = lambda: None

    def test(self, info):
        print(info)

    def test_favorite_item(self, item):
        return item.is_video() or item.is_thumb()

    def get_page_type(self):
        return FavoriteRecord.video

    def playback(self, media=MediaData(), page_url=URL(), autoplay=False):
        if Setting.video_info:
            print('Now playback', page_url)
            for item in media.alternate:
                print(item['text'], item['url'].get())
            print()

        self.player_url = media.url
        self.url = page_url
        self.video_player.set_url(self.player_url.get())
        self.setWindowTitle(self.player_url.get())
        self.controls.clear()

        for item in media.alternate:
            self.video_player.add_alternate_url(item['text'], item['url'].get())
        if autoplay:
            self.video_player.play()

    def playlist_connect(self, goto_prev=lambda: None, goto_next=lambda: None):
        self.video_player.connect_to_playlist(connected=True, goto_prev=goto_prev, goto_next=goto_next)
        self.prev = goto_prev
        self.next = goto_next

    def playlist_disconnect(self):
        self.video_player.connect_to_playlist(connected=False)
        self.prev = lambda: None
        self.next = lambda: None

    def delete_from_playlist(self):
        if Setting.view_debug: print('Delete', self.url.get(), 'from pos', self.controller.get_playlist().current_index)
        self.controller.get_playlist().delete_item(self.controller.get_playlist().current_index)
        self.video_player.stop()
        try:
            self.controller.goto_url(self.controller.get_playlist().current_entry.url)
        except PlaylistException:
            self.playlist_disconnect()

    def load_video(self, fname='', url=''):
        print(self.url.get())
        t = urlparse(self.url.get())[2].strip('/').split('/')
        prefix = t[len(t) - 1]
        self.controller.uget_file(filename=prefix + '_' + fname, url=URL(url + '*'))

    def on_error_handler(self, eroor_message):
        # print(eroor_message)
        self.manager.get_thumb_view().show_status(eroor_message)

    def panic(self):
        super().panic()
        self.video_player.stop()


if __name__ == "__main__":
    pass
