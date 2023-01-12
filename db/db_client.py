#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import os
import sys

from utils.six import urlparse, withMetaclass
from utils.singleton import Singleton

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DBClient(withMetaclass(Singleton)):
    """
    DBClient DB工厂类, 提供 get/put/update/pop/delete
    exists/get_all/clean/get_count/change_table方法

    抽象方法定义:
    get(): 随机返回一个proxy
    put(proxy): 存入一个proxy
    pop(): 顺序返回并删除一个proxy
    update(proxy): 更新指定proxy的信息
    delete(proxy): 删除一个指定的proxy
    exists(proxy): 判断指定的proxy是否存在
    get_all(): 返回所有的proxies
    clean(): 清除所有的代理信息
    get_count(): 返回proxy的数量
    change_table(name): 切换操作对象

    所有方法需要相应类去具体实现
    ssdb: ssdb_client.py
    redis: redisClient.py
    mongodb: mongodb_client.py

    """

    def __init__(self, db_conn):
        """
        init
        :return:
        """
        self.parse_db_conn(db_conn)
        self.__init_db_client()

    @classmethod
    def parse_db_conn(cls, db_conn):
        db_conf = urlparse(db_conn)
        cls.db_type = db_conf.scheme.upper().strip()
        cls.db_host = db_conf.hostname
        cls.db_port = db_conf.port
        cls.db_user = db_conf.username
        cls.db_pwd = db_conf.password
        cls.db_name = db_conf.path[1:]
        return cls

    def __init_db_client(self):
        """
        init DB Client
        :return:
        """
        __type = None
        if "SSDB" == self.db_type:
            __type = "ssdbClient"
        elif "REDIS" == self.db_type:
            __type = "redisClient"
        else:
            pass
        assert __type, 'type error, Not support DB type: {}'.format(self.db_type)
        self.client = getattr(__import__(__type), "%sClient" % self.db_type.title())(host=self.db_host,
                                                                                     port=self.db_port,
                                                                                     username=self.db_user,
                                                                                     password=self.db_pwd,
                                                                                     db=self.db_name)

    def get(self, https, **kwargs):
        return self.client.get(https, **kwargs)

    def put(self, key, **kwargs):
        return self.client.put(key, **kwargs)

    def update(self, key, value, **kwargs):
        return self.client.update(key, value, **kwargs)

    def delete(self, key, **kwargs):
        return self.client.delete(key, **kwargs)

    def exists(self, key, **kwargs):
        return self.client.exists(key, **kwargs)

    def pop(self, https, **kwargs):
        return self.client.pop(https, **kwargs)

    def get_all(self, https):
        return self.client.get_all(https)

    def clear(self):
        return self.client.clear()

    def change_table(self, name):
        self.client.change_table(name)

    def get_count(self):
        return self.client.get_count()

    def test(self):
        return self.client.test()
