#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from utils.six import Queue
from helper.fetch import Fetcher
from helper.check import checker
from handler.log_handler import LogHandler
from handler.proxy_handler import ProxyHandler
from handler.config_handler import ConfigHandler


def __run_proxy_fetch():
    proxy_queue = Queue()
    proxy_fetcher = Fetcher()

    for proxy in proxy_fetcher.run():
        proxy_queue.put(proxy)

    checker("raw", proxy_queue)


def __run_proxy_check():
    proxy_handler = ProxyHandler()
    proxy_queue = Queue()
    if proxy_handler.db.get_count().get("total", 0) < proxy_handler.conf.pool_size_min:
        __run_proxy_fetch()
    for proxy in proxy_handler.get_all():
        proxy_queue.put(proxy)
    checker("use", proxy_queue)


def run_scheduler():
    __run_proxy_fetch()

    timezone = ConfigHandler().timezone
    scheduler_log = LogHandler("scheduler")
    scheduler = BlockingScheduler(logger=scheduler_log, timezone=timezone)

    scheduler.add_job(__run_proxy_fetch, 'interval', minutes=4, id="proxy_fetch", name="proxy采集")
    scheduler.add_job(__run_proxy_check, 'interval', minutes=2, id="proxy_check", name="proxy检查")
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }

    scheduler.configure(executors=executors, job_defaults=job_defaults, timezone=timezone)

    scheduler.start()


if __name__ == '__main__':
    run_scheduler()
