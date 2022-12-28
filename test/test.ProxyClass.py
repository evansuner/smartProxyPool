#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import json
from helper.proxy import Proxy


def test_proxy():
    proxy = Proxy('127.0.0.1:8000')
    print(proxy.to_json)
    proxy.source = 'test'
    proxy.ping = '200ms'
    proxy_str = json.dumps(proxy.to_dict, ensure_ascii=False)
    print(proxy_str)
    print(Proxy.create_from_json(proxy_str).to_dict)


if __name__ == '__main__':
    test_proxy()
