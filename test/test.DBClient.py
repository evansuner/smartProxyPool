#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from db.db_client import DBClient


def test_client():
    redis_uri = 'redis://:123456@127.0.0.1:6379/1'
    r = DBClient.parse_db_conn(redis_uri)
    assert r.db_type == 'REDIS'
    assert r.db_password == '123456'
    assert r.db_host == '127.0.0.1'
    assert r.db_port == 6379
    assert r.db_name == '1'
    print('DBClient OK!')


if __name__ == '__main__':
    test_client()
