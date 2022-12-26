#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from re import findall
from requests import head
from requests.exceptions import Timeout
from utils.six import withMetaclass
from utils.singleton import Singleton
from handler.config_handler import ConfigHandler

conf = ConfigHandler()
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}


class ProxyValidator(withMetaclass(Singleton)):
    pre_validator = []
    http_validator = []
    https_validator = []

    @classmethod
    def add_pre_validator(cls, func):
        cls.pre_validator.append(func)
        return func

    @classmethod
    def add_http_validator(cls, func):
        cls.http_validator.append(func)
        return func

    @classmethod
    def add_https_validator(cls, func):
        cls.https_validator.append(func)
        return func


@ProxyValidator.add_pre_validator
def format_validator(proxy):
    """check the format of the proxy"""
    verify_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
    _proxy = findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


@ProxyValidator.add_http_validator
def http_timeout_validator(proxy):
    """http timeout checking"""
    proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
    try:
        r = head(conf.http_url, headers=HEADER, proxies=proxies, timeout=conf.verify_timeout)
        return True if r.status_code == 200 else False
    except Timeout as e:
        return False


@ProxyValidator.add_https_validator
def https_timeout_validator(proxy):
    """https timeout checking"""
    proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
    try:
        r = head(conf.http_url, headers=HEADER, proxies=proxies, timeout=conf.verify_timeout)
        return True if r.status_code == 200 else False
    except Timeout as e:
        return False


@ProxyValidator.add_https_validator
def custom_validator_example(proxy):
    """custom validator function, verify whether proxy could be used, function should return True/False"""
    return True
