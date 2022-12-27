#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from handler.config_handler import ConfigHandler
from time import sleep


def test_config():
    conf = ConfigHandler()
    print(conf.db_conn)
    print(conf.server_host)
    print(conf.server_port)
    print(conf.table_name)
    assert isinstance(conf.fetchers, list)
    print(conf.fetchers)

    for _ in range(2):
        print(conf.fetchers)
        sleep(5)


if __name__ == '__main__':
    test_config()
