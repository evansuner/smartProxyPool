#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import click
from helper.launcher import start_server, start_schedule
from settings import VERSION, BANNER

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """SmartProxyPool tool"""


@cli.command()
def schedule():
    """start scheduler programme"""
    start_schedule()


@cli.command()
def server():
    """start api server"""
    click.echo(BANNER)
    start_server()


if __name__ == '__main__':
    cli()
