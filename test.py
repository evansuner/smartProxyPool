#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from test import testProxyValidator
from test import testConfigHandler
from test import testLogHandler
from test import testDbClient

if __name__ == '__main__':
    print("ConfigHandler:")
    testConfigHandler.test_config()

    print("LogHandler:")
    testLogHandler.test_log_handler()

    print("DbClient:")
    testDbClient.test_db_client()

    print("ProxyValidator:")
    testProxyValidator.test_proxy_validator()
