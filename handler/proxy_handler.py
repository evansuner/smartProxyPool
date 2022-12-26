#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from helper.proxy import Proxy
from db.db_client import DBClient
from handler.config_handler import ConfigHandler


class ProxyHandler:
    """Proxy CURD operators"""

    def __init__(self) -> None:
        self.conf = ConfigHandler()
        self.db = DBClient(self.conf.db_conn)
        self.db.change_table(self.conf.table_name)

    def get(self, https: False):
        """
        return a proxy
        args:
            https: True/False
        Returns:
        """
        proxy = self.db.get(https)
        return Proxy.create_from_json(proxy) if proxy else None

    def pop(self, https):
        """return and delete a useful proxy"""
        proxy = self.db.pop(https)
        if proxy:
            return Proxy.create_from_json(proxy)
        return None

    def put(self, proxy):
        """
        put proxy into use proxy
        :return:
        """
        self.db.put(proxy)

    def delete(self, proxy):
        """
        delete useful proxy
        :param proxy:
        :return:
        """
        return self.db.delete(proxy.proxy)

    def get_all(self, https=False):
        """
        get all proxy from pool as Proxy list
        :return:
        """
        proxies = self.db.get_all(https)
        return [Proxy.create_from_json(_) for _ in proxies]

    def exists(self, proxy):
        """
        check proxy exists
        :param proxy:
        :return:
        """
        return self.db.exists(proxy.proxy)

    def get_count(self):
        """
        return raw_proxy and use_proxy count
        :return:
        """
        total_use_proxy = self.db.get_count()
        return {'count': total_use_proxy}
