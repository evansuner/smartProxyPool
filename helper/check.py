#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from queue import Empty
from threading import Thread
from datetime import datetime
from utils.web_request import WebRequest
from handler.log_handler import LogHandler
from handler.proxy_handler import ProxyHandler
from handler.config_handler import ConfigHandler
from helper.validator import ProxyValidator


class Validator:
    """do validating"""
    conf = ConfigHandler()

    @classmethod
    def validator(cls, proxy, work_type):
        """entrance of validator
        Args:
            proxy: proxy object
            work_type: raw/use
        returns:
            proxy obj
        """
        is_http = cls.http_validator(proxy)
        is_https = False if not is_http else cls.https_validator(proxy)
        proxy.check_count += 1
        proxy.last_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        proxy.last_status = True if is_https else False
        if is_http:
            if proxy.fail_count > 0:
                proxy.fail_count -= 1
            proxy.https = True if is_https else False
            if work_type == 'raw':
                proxy.region = cls.region_getter(proxy) if cls.conf.proxy_region else ''
            else:
                proxy.fail_count += 1
            return proxy

    @classmethod
    def http_validator(cls, proxy):
        for func in ProxyValidator.http_validator:
            if not func(proxy.proxy):
                return False
            return True

    @classmethod
    def https_validator(cls, proxy):
        for func in ProxyValidator.https_validator:
            if not func(proxy.proxy):
                return False
            return True

    @classmethod
    def pre_validator(cls, proxy):
        for func in ProxyValidator.pre_validator:
            if not func(proxy):
                return False
        return True

    @classmethod
    def region_getter(cls, proxy):
        try:
            url = f'https://searchplugin.csdn.net/api/v1/ip/get?ip={proxy.proxy.split(":")[0]}'
            r = WebRequest().get(url, retry_time=1, timeout=2).json
            return r['data']['address']
        except Exception:
            return 'error'


class _ThreadChecker(Thread):
    """multithread checking"""

    def __int__(self, work_type, target_queue, thread_name):
        Thread.__init__(self, name=thread_name, group=None)
        self.work_type = work_type
        self.log = LogHandler('checker')
        self.proxy_handler = ProxyHandler()
        self.target_queue = target_queue
        self.conf = ConfigHandler()

    def run(self) -> None:
        self.log.info(f'{self.work_type.title()} ProxyCheck - {self.name}: start')
        while True:
            try:
                proxy = self.target_queue.get(block=False)
            except Empty:
                self.log.info(f'{self.work_type.title()} ProxyCheck - {self.name}: complete')
                break
            proxy = Validator.validator(proxy, self.work_type)
            if self.work_type == 'raw':
                self.__if_raw(proxy)
            else:
                self.__if_use(proxy)
            self.target_queue.task_done()

    def __if_raw(self, proxy):
        if proxy.last_status:
            if self.proxy_handler.exists(proxy):
                self.log.info(f'RawProxyCheck - {self.name}: {proxy.proxy.ljust(23)} exist')
            else:
                self.log.info(f'RawProxyCheck - {self.name}: {proxy.proxy.ljust(23)} pass')
                self.proxy_handler.put(proxy)
        else:
            self.log.info(f'RawProxyCheck - {self.name}: {proxy.proxy.ljust(23)} failed')

    def __if_use(self, proxy):
        if proxy.last_status:
            self.log.info(f'UseProxyCheck - {self.name}: {proxy.proxy.ljust(23)} pass')
            self.proxy_handler.put(proxy)
        else:
            if proxy.fail_count > self.conf.maxFailCount:
                self.log.info(
                    f'UseProxyCheck - {self.name}: {proxy.proxy.ljust(23)} fail, count {proxy.fail_count} delete')
                self.proxy_handler.delete(proxy)
            else:
                self.log.info(
                    f'UseProxyCheck - {self.name}: {proxy.proxy.ljust(23)} fail, count {proxy.fail_count} keep')
                self.proxy_handler.put(proxy)


def checker(tp, queue):
    """
    run Proxy ThreadChecker
    :param tp: raw/use
    :param queue: Proxy Queue
    :return:
    """
    thread_list = list()
    for index in range(20):
        thread_list.append(_ThreadChecker(tp, queue, "thread_%s" % str(index).zfill(2)))

    for thread in thread_list:
        thread.setDaemon(True)
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    v = Validator()

