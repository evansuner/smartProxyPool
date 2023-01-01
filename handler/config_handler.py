#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))
import settings
from utils.singleton import Singleton
from utils.lazy_property import LazyProperty
from utils.six import withMetaclass


class ConfigHandler(withMetaclass(Singleton)):
    def __init__(self) -> None:
        pass

    @LazyProperty
    def server_host(self):
        return os.environ.get('HOST', settings.HOST)

    @LazyProperty
    def server_port(self):
        return os.environ.get('PORT', settings.PORT)

    @LazyProperty
    def db_conn(self):
        return os.environ.get('DB_CONN', settings.DB_CONN)

    @LazyProperty
    def table_name(self):
        return os.environ.get('TABLE_NAME', settings.TABLE_NAME)

    @LazyProperty
    def fetchers(self):
        return os.environ.get('PROXY_FETCHER', settings.PROXY_FETCHER)

    @LazyProperty
    def http_url(self):
        return os.environ.get('HTTP_URL', settings.HTTP_URL)

    @LazyProperty
    def https_url(self):
        return os.environ.get('HTTPS_URL', settings.HTTPS_URL)

    @LazyProperty
    def verify_timeout(self):
        return int(os.getenv("VERIFY_TIMEOUT", settings.VERIFY_TIMEOUT))

    # @LazyProperty
    # def proxyCheckCount(self):
    #     return int(os.getenv("PROXY_CHECK_COUNT", setting.PROXY_CHECK_COUNT))

    @LazyProperty
    def max_fail_count(self):
        return int(os.getenv("MAX_FAIL_COUNT", settings.MAX_FAIL_COUNT))

    # @LazyProperty
    # def maxFailRate(self):
    #     return int(os.getenv("MAX_FAIL_RATE", setting.MAX_FAIL_RATE))

    @LazyProperty
    def pool_size_min(self):
        return int(os.getenv("POOL_SIZE_MIN", settings.POOL_SIZE_MIN))

    @LazyProperty
    def proxy_region(self):
        return bool(os.getenv("PROXY_REGION", settings.PROXY_REGION))

    @LazyProperty
    def timezone(self):
        return os.getenv("TIMEZONE", settings.TIMEZONE)


if __name__ == '__main__':
    c = ConfigHandler()
    print(c.fetchers)
