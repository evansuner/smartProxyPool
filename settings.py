#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

BANNER = r"""
****************************************************************
*** ______  ********************* ______ *********** _  ********
*** | ___ \_ ******************** | ___ \ ********* | | ********
*** | |_/ / \__ __   __  _ __   _ | |_/ /___ * ___  | | ********
*** |  __/|  _// _ \ \ \/ /| | | ||  __// _ \ / _ \ | | ********
*** | |   | | | (_) | >  < \ |_| || |  | (_) | (_) || |___  ****
*** \_|   |_|  \___/ /_/\_\ \__  |\_|   \___/ \___/ \_____/ ****
****                       __ / /                          *****
************************* /___ / *******************************
*************************       ********************************
****************************************************************
"""

VERSION = "1.0"

# server config
HOST = '0.0.0.0'
PORT = 5010

# database config
DB_CONN = 'redis://:pwd@127.0.0.1/0'

TABLE_NAME = 'use_proxy'

# config the proxy fetch function
PROXY_FETCHER = [
    "freeProxy01",
    "freeProxy02",
    "freeProxy03",
    "freeProxy04",
    "freeProxy05",
    "freeProxy06",
    "freeProxy07",
    "freeProxy08",
    "freeProxy09",
    "freeProxy10",
]

# proxy_validator
# target url for validating
HTTP_URL = "http://httpbin.org"
HTTPS_URL = "https://www.qq.com"

# timeout for validator
VERIFY_TIMEOUT = 10
# maximum checking times otherwise delete the proxy
MAX_FAIL_COUNT = 0
# during proxy checking, it will handle schedule while less than POOL_SIZE_MIN
POLL_SIZE_MIN = 20

# proxy attributes
# turn on proxy region attributes
PROXY_REGION = True

# schedule config
TIMEZONE = "Asia/Shanghai"