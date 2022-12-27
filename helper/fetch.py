#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from threading import Thread
from helper.proxy import Proxy
from helper.check import Validator
from handler.log_handler import LogHandler
from handler.config_handler import ConfigHandler
from handler.proxy_handler import ProxyHandler
from fetcher.proxy_fetcher import ProxyFetcher


class _ThreadFetcher(Thread):
    def __init__(self, fetch_source, proxy_dict):
        Thread.__init__(self)
        self.fetch_source = fetch_source
        self.proxy_dict = proxy_dict
        self.fetcher = getattr(ProxyFetcher, fetch_source, None)
        self.log = LogHandler('fetcher')
        self.conf = ConfigHandler()
        self.proxy_handler = ProxyHandler()

    def run(self):
        self.log.info(f'ProxyFetch - {self.fetch_source}: start')
        try:
            for proxy in self.fetcher():
                self.log.info(f'ProxyFetch - {self.fetch_source}: {proxy.ljust(23)} success')
                proxy = proxy.strip()
                if proxy in self.proxy_dict:
                    self.proxy_dict[proxy].add_source(self.fetch_source)
                else:
                    self.proxy_dict[proxy] = Proxy(proxy, source=self.fetch_source)
        except Exception as e:
            self.log.error(f'ProxyFetch - {self.fetch_source}: error')
            self.log.error(str(e))


class Fetcher:
    name = 'fetcher'

    def __init__(self):
        self.log = LogHandler(self.name)
        self.conf = ConfigHandler()

    def run(self):
        """fetch proxy with proxy_fetchers"""
        proxy_dict = dict()
        thread_list = list()
        self.log.info("ProxyFetch: start")

        for fetch_source in self.conf.fetchers:
            self.log.info(f'ProxyFetch - {fetch_source}: start')
            fetcher = getattr(ProxyFetcher, fetch_source, None)
            if not fetcher:
                self.log.error(f'ProxyFetch - {fetch_source}: class method not exists!')
                continue
            if not callable(fetcher):
                self.log.error(f'ProxyFetch - {fetch_source}: must be class method')
            thread_list.append(_ThreadFetcher(fetch_source, proxy_dict))
        for thread in thread_list:
            thread.setDaemon(True)
            thread.start()
        for thread in thread_list:
            thread.join()

        self.log.info('ProxyFetch - all complete!')
        for _ in proxy_dict.values():
            if Validator.pre_validator(_.proxy):
                yield _
