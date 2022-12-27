#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from handler.log_handler import LogHandler


def test_handler():
    log = LogHandler('test')
    log.info('this is test info')
    log.error('this is test error')


if __name__ == '__main__':
    test_handler()
