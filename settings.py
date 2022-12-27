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
DB_CONN = 'redis://:123456@127.0.0.1:6379/0'

TABLE_NAME = 'use_proxy'

# config the proxy fetch function
PROXY_FETCHER = [
    "free_proxy01",
    "free_proxy02",
    "free_proxy03",
    "free_proxy04",
    "free_proxy05",
    "free_proxy06",
    "free_proxy07",
    # "free_proxy08",
    "free_proxy09",
    "free_proxy10",

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
POLL_SIZE_MIN = 10

# proxy attributes
# turn on proxy region attributes
PROXY_REGION = True

# schedule config
TIMEZONE = "Asia/Shanghai"
