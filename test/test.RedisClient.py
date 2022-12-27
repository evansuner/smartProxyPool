#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from db.db_client import DBClient
from helper.proxy import Proxy


def test_client():
    uri = 'redis://:123456@127.0.0.1:6379'
    db = DBClient(uri)
    db.change_table('use_proxy')
    proxy = Proxy.create_from_json(
        '{"proxy": "118.190.79.36:8090", "https": false, "fail_count": 0, "region": "", "anonymous": "", "source": '
        '"freeProxy02", "check_count": 4, "last_status": true, "last_time": "2022-12-27 15:58:04"}')
    print('put: ', db.put(proxy))
    print('get: ', db.get(https=None))
    print('exists: ', db.exists("27.38.96.101:9797"))
    print('exists: ', db.exists("118.190.79.36:8090"))
    print('pop: ', db.pop(https=True))
    db.clear()
    print('get_all: ', db.get_all(https=None))
    print('get_count: ', db.get_count())


if __name__ == '__main__':
    test_client()
