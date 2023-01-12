#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import os
import settings
from utils.singleton import Singleton
from utils.lazy_property import LazyProperty
from utils.six import reload_six, withMetaclass


class ConfigHandler(withMetaclass(Singleton)):

    def __init__(self):
        pass

    @LazyProperty
    def server_host(self):
        return os.environ.get("HOST", settings.HOST)

    @LazyProperty
    def server_port(self):
        return os.environ.get("PORT", settings.PORT)

    @LazyProperty
    def db_conn(self):
        return os.getenv("DB_CONN", settings.DB_CONN)

    @LazyProperty
    def table_name(self):
        return os.getenv("TABLE_NAME", settings.TABLE_NAME)

    @property
    def fetchers(self):
        reload_six(settings)
        return settings.PROXY_FETCHER

    @LazyProperty
    def http_url(self):
        return os.getenv("HTTP_URL", settings.HTTP_URL)

    @LazyProperty
    def https_url(self):
        return os.getenv("HTTPS_URL", settings.HTTPS_URL)

    @LazyProperty
    def verify_timeout(self):
        return int(os.getenv("VERIFY_TIMEOUT", settings.VERIFY_TIMEOUT))

    @LazyProperty
    def max_fail_count(self):
        return int(os.getenv("MAX_FAIL_COUNT", settings.MAX_FAIL_COUNT))

    @LazyProperty
    def pool_size_min(self):
        return int(os.getenv("POOL_SIZE_MIN", settings.POOL_SIZE_MIN))

    @LazyProperty
    def proxy_region(self):
        return bool(os.getenv("PROXY_REGION", settings.PROXY_REGION))

    @LazyProperty
    def timezone(self):
        return os.getenv("TIMEZONE", settings.TIMEZONE)

