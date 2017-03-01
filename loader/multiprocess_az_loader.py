# -*- coding: utf-8 -*-
__author__ = 'Vit'

import datetime
import json
import os
import re
from io import StringIO
from multiprocessing import Manager, Queue, Process, Lock

import requests

from loader.base_loader import BaseLoader, BaseLoadProcess, URL, LoaderError, FLData, PictureCollector, \
    PictureCollectorException, BaseLoadProcedure
from loader.request_load import RequestLoad
from loader.trick_load import TrickLoad
from setting import Setting


class DataServer:
    def __init__(self):
        self.manager = Manager()
        self.data = self.manager.dict()
        self.last_load_proxy_pack = None
        self.init_data()
        # print('Proxy pack', len(self.data['proxy_domains']))

    def get_data(self):
        return self.data

    def stop(self):
        self.write_config(Setting.base_dir + 'az.json')
        self.manager.shutdown()

    def init_data(self):
        print('Requests version: ' + requests.__version__)
        self.read_config(Setting.base_dir + 'az.json')
        self.read_proxy_pac(URL("http://antizapret.prostovpn.org/proxy.pac*"))
        self.data['domain_cash'] = dict()

    def read_proxy_pac(self, pac_url):
        if self.last_load_proxy_pack:
            if datetime.datetime.now() - self.last_load_proxy_pack < datetime.timedelta(hours=2):
                return
        try:
            print('loading', pac_url)
            pac = RequestLoad().open(pac_url).decode()

            r = re.search('\"PROXY (.*); DIRECT', pac)
            if r:
                self.data['free_http_proxy'] = r.group(1)
                # p = re.findall("\"(.*?)\",", pac)
                #
                # proxy_domains = list()
                # for item in p:
                #     proxy_domains.append(item)
                # self.data['proxy_domains']=proxy_domains

            self.last_load_proxy_pack = datetime.datetime.now()

        except LoaderError:
            print('AZLoader error:', pac_url, 'not loaded')

    def read_config(self, config_filename):
        try:
            with open(config_filename) as config:
                data = json.load(config)
                self.data['free_http_proxy'] = data.get('free_http_proxy', None)
                self.data['proxy_domains'] = data.get('proxy_domains', list())
                self.last_load_proxy_pack = datetime.datetime.fromtimestamp(data.get('last_loaded'), None)

        except EnvironmentError as err:
            print('Read ' + config_filename + ' error: ', err)
        except (TypeError, ValueError):
            print('DataServer config error, using default')
            self.last_load_proxy_pack = None

    def write_config(self, config_filename):
        try:
            os.replace(config_filename, config_filename + '.old')
        except EnvironmentError as err:
            print('Writing ' + config_filename + ' error: ', err)

        try:
            with open(config_filename, 'w') as config:
                # print('Writing DataServer config to ' + config_filename)

                data = dict()
                data['free_http_proxy'] = self.data['free_http_proxy']
                data['last_loaded'] = self.last_load_proxy_pack.timestamp()
                data['proxy_domains'] = self.data.get('proxy_domains', list())

                json.dump(data, config)
        except EnvironmentError as err:
            print('Writing ' + config_filename + ' error: ', err)


class AZloaderMP(BaseLoadProcedure):
    def __init__(self, data, lock:Lock):
        self.data = data
        self.lock = lock
        self.request_load = RequestLoad()
        self.trick_load = TrickLoad()

    def open(self, url: URL) -> bytes:
        method = self.get_load_method(url)

        if method == 'none':
            raise LoaderError('No way to open, connection not established or content filtered.')

        if method == 'plain':
            self.request_load.proxies = None
            return self.request_load.open(url)
        elif method == 'proxy':
            self.request_load.proxies = {'http': self.data.get('free_http_proxy', '')}
            return self.request_load.open(url)
        else:
            return self.trick_load.open(url,method)

    def get_load_method(self, url: URL) -> str:
        domain_cash = self.data.get('domain_cash', dict())
        domain = url.domain()
        for item in domain_cash:
            if '.' + item in domain or item == domain:
                return domain_cash[item]

        if url.test_string is None:
            return 'plain'

        print('Testing domain:', domain, '... ')
        method = self._inspect_availability(url)
        print('            ...', method)

        self.lock.acquire()
        domain_cash = self.data.get('domain_cash', dict())
        if domain.startswith('www.'):
            domain=domain.partition('.')[2]
        domain_cash[domain] = method
        self.data['domain_cash'] = domain_cash
        print(domain_cash)
        self.lock.release()

        return method

    def _inspect_availability(self, url: URL) -> str:
        self.request_load.proxies = None
        try:
            string = self.request_load.open(url).decode()

            if url.test_string in string:
                return 'plain'
        except LoaderError:
            pass

        try:
            self.request_load.proxies = {'http': self.data.get('free_http_proxy', '')}
            string = self.request_load.open(url).decode()

            if url.test_string in string:
                return 'proxy'
        except LoaderError:
            pass

        for method_name in self.trick_load.trick_headers:
            # print(method_name)
            string = self.trick_load.open(url,trick=method_name).decode()
            # print(string)
            if url.test_string in string:
                return method_name

        return 'none'


class FLEvent():
    def __init__(self, type: str, data=None):
        self.event_type = type
        self.event_data = data

    def type(self):
        return self.event_type

    def data(self):
        return self.event_data


class LoadServer(Process):
    def __init__(self,
                 fldata_list: list,
                 events_queue: Queue,
                 picture_collector: PictureCollector,
                 data_server: DataServer,
                 lock: Lock):
        self.filelist = fldata_list
        self.events = events_queue
        self.collector = picture_collector
        self.data = data_server.get_data()
        self.lock = lock
        Process.__init__(self)

    def run(self):
        self.events.put(FLEvent('start'))
        loader = AZloaderMP(self.data, self.lock)

        for filedata in self.filelist:
            try:
                if self.collector is not None:
                    # print(item.get_url().get())
                    bytes = loader.open(filedata.get_url())
                    filedata.set_url(URL(self.collector.parse_index(StringIO(bytes.decode()), filedata.get_url())))
                    if self.collector.get_type() == 'iter':
                        self.filelist.append(self.collector.next())

                result=loader.load_to_file(filedata)
                self.events.put(FLEvent('load', result))
            except (ValueError, LoaderError) as Error:
                self.events.put(FLEvent('error', filedata))
                print(filedata.get_url().get() + ' not loaded: ', Error)
            except PictureCollectorException:
                print(item.get_url().get() + ' not loaded: PictureCollector Error')
        self.events.put(FLEvent('done'))


class LoadProcess(BaseLoadProcess):
    def __init__(self, on_load_handler, on_end_handler, data_server: DataServer, lock: Lock):
        self.loader = None
        self.events_queue = Queue()
        self.on_load = on_load_handler
        self.on_end = on_end_handler
        self.data_server = data_server
        self.lock = lock

    def load_list(self, fldata_list: list, picture_collector: PictureCollector = None):
        self.loader = LoadServer(fldata_list, self.events_queue, picture_collector, self.data_server, self.lock)
        self.loader.start()

    def update(self):
        if self.events_queue:
            while not self.events_queue.empty():
                event = self.events_queue.get()

                if event.type() == 'load':
                    self.on_load(event.data())

                if event.type() == 'done':
                    self.on_end()

    def abort(self):
        if self.loader is not None:
            self.loader.terminate()
            self.update()


class MultiprocessAZloader(BaseLoader):
    def __init__(self):
        self.data = DataServer()
        self.lock = Lock()
        self.list_of_load_process = list()
        self.single_file_loader = None

    def get_new_load_process(self, on_load_handler=lambda filedata: None,
                             on_end_handler=lambda: None) -> BaseLoadProcess:
        new_process = LoadProcess(on_load_handler=on_load_handler,
                                  on_end_handler=on_end_handler,
                                  data_server=self.data,
                                  lock=self.lock)
        self.list_of_load_process.append(new_process)
        return new_process

    def on_update(self):
        if self.single_file_loader:
            self.single_file_loader.update()
        for load_process in self.list_of_load_process:
            load_process.update()

    def start_load_file(self, filedata: FLData, on_result=lambda filedata: None):
        if self.single_file_loader:
            self.single_file_loader.abort()
        self.single_file_loader = LoadProcess(on_load_handler=on_result,
                                              on_end_handler=lambda: None,
                                              data_server=self.data,
                                              lock=self.lock)
        self.single_file_loader.load_list([filedata])

    def on_exit(self):
        self.data.stop()
        for load_process in self.list_of_load_process:
            load_process.abort()


if __name__ == "__main__":
    import time

    print(Setting.base_dir)
    # l= RequestLoad()
    # url=URL('http://scs.spb.ru')
    # print(l.open(url).decode())

    print()

    l=MultiprocessAZloader()
    # ds = DataServer()
    time.sleep(5)

    for item in ds.data['proxy_domains']:
        print(item)

    time.sleep(5)

    ds.stop()
