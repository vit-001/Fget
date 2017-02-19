__author__ = 'Vit'

from loader.base_loader import URL


class PlaylistEntry():
    def __init__(self, url=URL()):
        self.url = url

    @property
    def save_line(self):
        return self.url.to_save()

    @staticmethod
    def get_from_save_line(save_line=''):
        return PlaylistEntry(URL(save_line))


class PlaylistException(Exception):
    pass


class Playlist():
    def __init__(self, file=None):
        self.list = list()
        self.current_index = 0
        self.on_change_listeners = list()
        self.on_change_index_listeners = list()

        if file is not None:
            for line in file:
                if line.strip('\n ') != '':
                    # print('"',line.strip(),'"')
                    item = PlaylistEntry.get_from_save_line(line.strip())
                    self.add(item)

    def add_listeners(self, on_change_listener=lambda: None,
                      on_change_index_listener=lambda index: None):
        self.on_change_listeners.append(on_change_listener)
        self.on_change_index_listeners.append(on_change_index_listener)

    def clear(self):
        self.list = list()
        self.current_index = 0
        for listener in self.on_change_listeners:
            listener()

    def add(self, item=PlaylistEntry()):
        self.list.append(item)
        for listener in self.on_change_listeners:
            listener()

    def next(self):
        self.current_index += 1
        if self.current_index > len(self.list) - 1:
            self.current_index = 0
        for listener in self.on_change_index_listeners:
            listener(self.current_index)

    def prev(self, silent=False):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = 0
        if silent: return
        for listener in self.on_change_index_listeners:
            listener(self.current_index)

    @property
    def current_entry(self):
        if len(self.list) == 0:
            raise PlaylistException()
        return self.list[self.current_index]

    def delete_items(self, indexes):
        for i in sorted(indexes, reverse=True):
            self.delete_item(i)
            #     r=self.list.pop(i)
            #     print(i,r)
            #
            # for listener in self.on_change_listeners:
            #     listener()

    def delete_item(self, index):
        if index < 0 or index >= len(self.list):
            return
        r = self.list.pop(index)
        # print(index,r.url)

        if index < self.current_index:
            self.prev(silent=True)

        if self.current_index >= len(self.list):
            self.current_index = len(self.list) - 1

        for listener in self.on_change_listeners:
            listener()

    def save(self, file):
        for item in self.list:
            file.write(item.save_line + '\n')

    def open(self, file):
        self.clear()
        for line in file:
            if line.strip('\n ') != '':
                item = PlaylistEntry.get_from_save_line(line.strip())
                self.add(item)
