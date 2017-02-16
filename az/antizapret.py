# -*- coding: utf-8 -*-

import os
import re
import fnmatch
import threading
# import urllib2
# import xbmc
# import xbmcaddon
from contextlib import contextmanager, closing

from urllib.request import ProxyHandler,Request,urlopen,HTTPError
from urllib.parse import urlencode


# __addon__ = xbmcaddon.Addon()
# CACHE_DIR = xbmc.translatePath(__addon__.getAddonInfo("profile"))
PAC_URL = "http://antizapret.prostovpn.org/proxy.pac"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"
CACHE = 24 * 3600  # 24 hour caching
LOCKS = {}
_config = {}
_custom_hosts = []


# if not os.path.exists(CACHE_DIR):
#     os.makedirs(CACHE_DIR)


# @contextmanager
# def shelf(filename, ttl=0):
#     import shelve
#     filename = os.path.join(CACHE_DIR, filename)
#     with LOCKS.get(filename, threading.RLock()):
#         with closing(shelve.open(filename, writeback=True)) as d:
#             import time
#             if not d:
#                 d.update({
#                     "created_at": time.time(),
#                     "data": {},
#                 })
#             elif ttl > 0 and (time.time() - d["created_at"]) > ttl:
#                 d.update({
#                     "created_at": time.time(),
#                     "data": {},
#                 })
#             yield d["data"]



def config():
    global _config
    try:
        data = urlopen(PAC_URL).read()
    except:
        data = ""

    r = re.search(b"\"PROXY (.*); DIRECT", data)
    pac = {"server": None,"domains": []}
    if r:
        pac["server"] = r.group(1)
        pac["domains"] = map(lambda x: x.replace(b"\Z(?ms)", "").replace("\\", ""), map(fnmatch.translate, re.findall(b"\"(.*?)\",", data)))

    _config = pac
    return _config

#
# def config_add(host):
#     host = host.split(':')[0]
#     if host not in _custom_hosts:
#         _custom_hosts.append(host)


class AntizapretProxyHandler(ProxyHandler, object):

    def __init__(self):
        self.config = config()
        ProxyHandler.__init__(self, {
            "http": "<empty>",
            "https": "<empty>",
            "ftp": "<empty>",
        })

    def proxy_open(self, req, proxy, type):
        import socket
        global _custom_hosts

        host = req.get_host().split(":")[0]
        # if self.config["server"] and (host in self.config["domains"] or socket.gethostbyname(host) in self.config["domains"] or host in _custom_hosts):
            # xbmc.log("[script.module.antizapret]: Pass request through proxy " + self.config["server"], level=xbmc.LOGDEBUG)
        return ProxyHandler.proxy_open(self, req, self.config["server"], type)

        # return None


def url_get(url, params={}, headers={}, post=None):

    if params:
        import urllib
        url = "%s?%s" % (url, urlencode(params))

    if post:
        import urllib
        post = urlencode(post)

    req = Request(url, post)
    req.add_header("User-Agent", USER_AGENT)

    for k, v in headers.items():
        req.add_header(k, v)

    try:
        with closing(urlopen(req)) as response:
            data = response.read()
            if response.headers.get("Content-Encoding", "") == "gzip":
                import zlib
                return zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
            return data
    except HTTPError as e:
        # xbmc.log("[script.module.antizapret]: HTTP Error(%s): %s" % (e.errno, e.strerror), level=xbmc.LOGERROR)
        return None
