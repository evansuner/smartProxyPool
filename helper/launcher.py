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
    from api.api import run_fastapi
    run_fastapi()


def start_schedule():
    __before_start()
    from helper.scheduler import run_scheduler
    run_scheduler()


def __before_start():
    __show_version()
    __show_configure()
    if __check_db_config():
        log.info('exit!')
        sys.exit()


def __show_version():
    from settings import VERSION
    log.info(f"ProxyPool Version: {VERSION}")


def __show_configure():
    conf = ConfigHandler()
    log.info(f"ProxyPool configure HOST: {conf.server_host}")
    log.info(f"ProxyPool configure PORT: {conf.server_port}")
    log.info(f"ProxyPool configure PROXY_FETCHER: {conf.fetchers}")


def __check_db_config():
    conf = ConfigHandler()
    db = DBClient(conf.db_conn)
    log.info("============ DATABASE CONFIGURE ================")
    log.info(f"DB_TYPE: {db.db_type}")
    log.info(f"DB_HOST: {db.db_host}")
    log.info(f"DB_PORT: {db.db_port}")
    log.info(f"DB_NAME: {db.db_name}")
    log.info(f"DB_USER: {db.db_user}")
    log.info("=================================================")
    return db.test()
