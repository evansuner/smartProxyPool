#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from fetcher.proxy_fetcher import ProxyFetcher
from handler.config_handler import ConfigHandler


def test_proxy_fetcher():
    conf = ConfigHandler()
    proxy_getter_functions = conf.fetchers
    proxy_counter = {_: 0 for _ in proxy_getter_functions}
    for proxyGetter in proxy_getter_functions:
        for proxy in getattr(ProxyFetcher, proxyGetter.strip())():
            if proxy:
                print('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                proxy_counter[proxyGetter] = proxy_counter.get(proxyGetter) + 1
    for key, value in proxy_counter.items():
        print(key, value)


if __name__ == '__main__':
    test_proxy_fetcher()
