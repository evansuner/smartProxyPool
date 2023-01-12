#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from db.db_client import DBClient


def test_db_client():
    #  ############### ssdb ###############
    ssdb_uri = "ssdb://:password@127.0.0.1:8888"
    s = DBClient.parse_db_conn(ssdb_uri)
    assert s.db_type == "SSDB"
    assert s.db_pwd == "password"
    assert s.db_host == "127.0.0.1"
    assert s.db_port == 8888

    #  ############### redis ###############
    redis_uri = "redis://:password@127.0.0.1:6379/1"
    r = DBClient.parse_db_conn(redis_uri)
    assert r.db_type == "REDIS"
    assert r.db_pwd == "password"
    assert r.db_host == "127.0.0.1"
    assert r.db_port == 6379
    assert r.db_name == "1"
    print("DbClient ok!")


if __name__ == '__main__':
    test_db_client()
