#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import sys
from db.db_client import DBClient
from handler.log_handler import LogHandler
from handler.config_handler import ConfigHandler

log = LogHandler('launcher')

def start_server():
    __before_start()
    from api.proxy_api import run_fastapi

def __before_start():
    pass