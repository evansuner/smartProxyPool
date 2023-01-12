#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from redis.exceptions import TimeoutError, ConnectionError, ResponseError
from redis.connection import BlockingConnectionPool
from handler.log_handler import LogHandler
from random import choice
from redis import Redis
import json


class RedisClient(object):
    """
    Redis client
    redis中存放结构的hash:
    key为ip:port, value为代理属性的字典
    """

    def __init__(self, **kwargs):
        """
        init
        :param host: host
        :param port: port
        :param password: password
        :param db: db
        :return:
        """
        self.name = ""
        kwargs.pop("username")
        self.__conn = Redis(connection_pool=BlockingConnectionPool(decode_responses=True,
                                                                   timeout=5,
                                                                   socket_timeout=5,
                                                                   **kwargs))

    def get(self, https):
        """
        return a proxy
        :return:
        """
        if https:
            items = self.__conn.hvals(self.name)
            proxies = list(filter(lambda x: json.loads(x).get("https"), items))
            return choice(proxies) if proxies else None
        else:
            proxies = self.__conn.hkeys(self.name)
            proxy = choice(proxies) if proxies else None
            return self.__conn.hget(self.name, proxy) if proxy else None

    def put(self, proxy_obj):
        """
        put proxy into hash, use change_table
        :param proxy_obj: Proxy obj
        :return:
        """
        data = self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)
        return data

    def pop(self, https):
        """
        get and remove a proxy from pool
        :return: dict {proxy: value}
        """
        proxy = self.get(https)
        if proxy:
            self.__conn.hdel(self.name, json.loads(proxy).get("proxy", ""))
        return proxy if proxy else None

    def delete(self, proxy_str):
        """
        remove specified proxy, use change_table determine hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hdel(self.name, proxy_str)

    def exists(self, proxy_str):
        """
        determine whether the proxy exists
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hexists(self.name, proxy_str)

    def update(self, proxy_obj):
        """
        update proxy attributes
        :param proxy_obj:
        :return:
        """
        return self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)

    def get_all(self, https):
        """
        return all proxies, use change_table determine hash name
        :return:
        """
        items = self.__conn.hvals(self.name)
        if https:
            return list(filter(lambda x: json.loads(x).get("https"), items))
        else:
            return items

    def clear(self):
        """
        clear all proxies, use change_table determine hash name
        :return:
        """
        return self.__conn.delete(self.name)

    def get_count(self):
        """
        count all proxies, use change_table determine hash name
        :return:
        """
        proxies = self.get_all(https=False)
        return {'total': len(proxies), 'https': len(list(filter(lambda x: json.loads(x).get("https"), proxies)))}

    def change_table(self, name):
        """
        change operate object
        :param name:
        :return:
        """
        self.name = name

    def test(self):
        log = LogHandler('redis_client')
        try:
            self.get_count()
        except TimeoutError as e:
            log.error(f'redis connection time out: {str(e)}', exc_info=True)
            return e
        except ConnectionError as e:
            log.error(f'redis connection error: {str(e)}', exc_info=True)
            return e
        except ResponseError as e:
            log.error(f'redis connection error: {str(e)}', exc_info=True)
            return e


