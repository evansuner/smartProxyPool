#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from fetcher.proxy_fetcher import ProxyFetcher
from handler.config_handler import ConfigHandler


def test_fetcher():
    conf = ConfigHandler()
    proxy_getter_functions = conf.fetchers
    proxy_counter = {_: 0 for _ in proxy_getter_functions}
    for proxy_getter in proxy_getter_functions:
        for proxy in getattr(ProxyFetcher, proxy_getter.strip())():
            if proxy:
                print(f'{proxy_getter}: fetch proxy {proxy}')
                proxy_counter[proxy_getter] = proxy_counter.get(proxy_getter) + 1
    for key, value in proxy_counter.items():
        print(key, value)


if __name__ == '__main__':
    test_fetcher()
