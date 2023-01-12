#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from helper.validator import ProxyValidator


def test_proxy_validator():
    for _ in ProxyValidator.pre_validator:
        print(_)
    for _ in ProxyValidator.http_validator:
        print(_)
    for _ in ProxyValidator.https_validator:
        print(_)


if __name__ == '__main__':
    test_proxy_validator()
