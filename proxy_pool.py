#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import click
from helper.launcher import start_server, start_scheduler
from settings import VERSION, BANNER

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """SmartProxyPool tool"""


@click.command(name='schedule')
def schedule():
    """start scheduler programe"""
    click.echo(BANNER)
    start_scheduler()


@click.command(name='server')
def server():
    """start api server"""
    click.echo(BANNER)
    start_server()


if __name__ == '__main__':
    cli()
