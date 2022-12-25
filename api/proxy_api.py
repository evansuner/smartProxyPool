#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import sys
from os.path import dirname, abspath
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from typing import Union

from utils.six import iteritems
from helper.proxy import Proxy
from handler.proxy_handler import ProxyHandler
from handler.config_handler import ConfigHandler

app = FastAPI()
conf = ConfigHandler()
proxy_handler = ProxyHandler()

api_list = [
    {"url": "/get", "params": "type: ''https'|''", "desc": "get a proxy"},
    {"url": "/pop", "params": "", "desc": "get and delete a proxy"},
    {"url": "/delete", "params": "proxy: 'e.g. 127.0.0.1:8080'", "desc": "delete an unable proxy"},
    {"url": "/all", "params": "type: ''https'|''", "desc": "get all proxy from proxy pool"},
    {"url": "/count", "params": "", "desc": "return proxy count"}
]
@app.get('/')
async def index():
    return {'url': api_list}

@app.get('/get')
async def get(request: Request):
    # https = request.arg
    pass

@app.get('/pop')
async def pop():
    pass

@app.get('/refresh')
async def refresh():
    pass

@app.get('/all')
async def get_all():
    pass

@app.get('/delete')
async def delete():
    pass

@app.get('/count')
async def count():
    pass

def run_fastapi():
    uvicorn.run(app, host=conf.server_host, port=conf.server_port, reload=True)

if __name__ == '__main__':
    run_fastapi()