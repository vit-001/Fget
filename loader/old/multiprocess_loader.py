__author__ = 'Vit'

from io import StringIO
from multiprocessing import Process, Queue, Event

from loader.base_loader import URL, FLData, BaseLoader
from loader.old.az_loader import AZLoader, LoaderError

class FLEvent():
    def __init__(self, type:str, data=None):
        self.event_type = type
        self.event_data = data

    def type(self):
        return self.event_type

    def data(self):
        return self.event_data

# class FLData():
#     def __init__(self, url:URL, filename:str):
#         self.url = url
#         self.filename = filename
#
#     def get_url(self):
#         return self.url
#
#     def get_filename(self):
#         return self.filename

class PictureCollectorException(Exception):
    pass

class PictureCollector():
    def __init__(self):
        self.type = 'simple'

    def get_type(self):
        return self.type

    def next(self):
        raise PictureCollectorException()

    def parse_index(self, iter_line, url:URL):
        raise PictureCollectorException()


class LoadServer(Process):
    def __init__(self, fldata_list:list, events:Queue, collector:PictureCollector=None):
        self.filelist = fldata_list
        self.events = events
        self.collector = collector
        self.az_loader=AZLoader()
        Process.__init__(self)

    def run(self):
        self.events.put(FLEvent('start'))
        print('Starting load', len(AZLoader.proxy_domains),len(AZLoader.trick_headers))

        for item in self.filelist:
            try:
                if self.collector is not None:
                    print(item.get_url().get())
                    response = self.az_loader.load(item.get_url())
                    picture_url = URL(self.collector.parse_index(StringIO(response), item.get_url()))
                    if self.collector.get_type() == 'iter':
                        self.filelist.append(self.collector.next())
                else:
                    picture_url = item.get_url()

                self.az_loader.load(picture_url, item.get_filename(), overwrite=False)
                self.events.put(FLEvent('load', item))
            except (ValueError, LoaderError) as Error:
                self.events.put(FLEvent('error', item))
                print(item.get_url().get() + ' not loaded: ', Error)
            except PictureCollectorException:
                print(item.get_url().get() + ' not loaded: PictureCollector Error')
        # print('Finishing')
        self.events.put(FLEvent('done'))


class LoadThread():
    def __init__(self, on_load_handler=lambda data: None, on_end_handler=lambda: None):
        self.loader = None
        self.events = Queue()
        self.on_load = on_load_handler
        self.on_end = on_end_handler

    def load_list(self, fldata_list:list, picture_collector:PictureCollector=None):
        self.loader = LoadServer(fldata_list, self.events, picture_collector)
        self.loader.start()

    def abort(self):
        if self.loader is not None:
            self.loader.terminate()
            self.update()

    def update(self):
        if self.events is not None:
            while not self.events.empty():
                event = self.events.get()
                if event.type() == 'load':
                    self.on_load(event.data())

                if event.type() == 'done':
                    self.on_end()


class SingleLoadServer(Process):
    def __init__(self, url:URL, filename:str, loaded:Event):
        self.fname = filename
        self.url = url
        self.loaded = loaded
        self.az_loader=AZLoader()
        Process.__init__(self)

    def run(self):
        # print('Starting load',self.url.get(),'to',self.fname)
        try:
            self.az_loader.safe_load(self.url, self.fname, overwrite=True)
            self.loaded.set()
        except (ValueError) as Error:
            print(self.url.get() + ' not loaded: ', Error)
            # print('Loading')


class SingleFileLoadThread():
    def __init__(self):
        self.loaded = Event()
        self.loader = None

    def load_file(self, url:URL, filename:str):
        self.abort()
        self.loader = SingleLoadServer(url, filename, self.loaded)
        self.fname = filename
        self.url = url
        self.loader.run()

    def abort(self):
        if self.loader is not None:
            if self.loader.is_alive():
                self.loader.terminate()
        self.loaded.clear()

    def is_loaded(self):
        if self.loaded.is_set():
            self.loaded.clear()
            return True
        else:
            return False

    def get_filename(self):
        return self.fname

    def get_url(self):
        return self.url


class Loader(BaseLoader):
    def __init__(self):
        self.threads = []
        self.single_thread = SingleFileLoadThread()
        self.on_result = lambda url, fname: None
        AZLoader()


    def get_new_load_process(self, on_load_handler=lambda x: None, on_end_handler=lambda: None):
        thread = LoadThread(on_load_handler, on_end_handler)
        self.threads.append(thread)
        return thread

    def load_list(self, thread=LoadThread(), lst=list(), picture_collector=None):
        thread.load_list(lst, picture_collector)

    def start_load_file(self, filedata:FLData, on_result=lambda filedata: None):
        # print('loading', url.get())
        self.single_thread.abort()
        self.on_result = on_result
        self.single_thread.load_file(filedata.get_url(), filedata.get_filename())

    def on_update(self):
        for item in self.threads:
            item.update()
        if self.single_thread.is_loaded():
            self.on_result(self.single_thread.get_url(), self.single_thread.get_filename())

    def on_exit(self):
        for thread in self.threads:
            thread.abort()


if __name__ == "__main__":
    pass
