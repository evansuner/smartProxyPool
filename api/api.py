#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import sys
from os.path import dirname, abspath
from typing import Union

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, FileResponse, Response
import uvicorn
from helper.proxy import Proxy
from handler.proxy_handler import ProxyHandler
from handler.config_handler import ConfigHandler

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


conf = ConfigHandler()
proxy_handler = ProxyHandler()

api_list = [
    {"url": "/get", "params": "type: ''https'|''", "desc": "get a proxy"},
    {"url": "/pop", "params": "", "desc": "get and delete a proxy"},
    {"url": "/delete", "params": "proxy: 'e.g. 127.0.0.1:8080'", "desc": "delete an unable proxy"},
    {"url": "/all", "params": "type: ''https'|''", "desc": "get all proxy from proxy pool"},
    {"url": "/count", "params": "", "desc": "return proxy count"}
]

favicon_path = 'static/favicon.ico'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get('/')
async def index():
    data = api_list
    return success(data=data)


@app.get('/get')
async def get(request: Request):
    https = request.method.lower() == 'https'
    proxy = proxy_handler.get(https)
    if proxy:
        data = proxy.to_dict
        return success(data=data)
    else:
        return error(message='NO PROXY')


@app.get('/pop')
async def pop(request: Request):
    https = request.method.lower() == 'https'
    proxy = proxy_handler.pop(https)
    if proxy:
        data = proxy.to_dict
        return success(data=data)
    else:
        return error(message='NO PROXY')


@app.get('/refresh')
async def refresh():
    # TODO refresh会有守护程序定时执行，由api直接调用性能较差，暂不使用
    return 'success'


@app.get('/all')
async def get_all(request: Request):
    https = request.method.lower() == 'https'
    proxies = proxy_handler.get_all(https)
    data = [_.to_dict for _ in proxies]
    return success(data=data)


@app.get('/delete')
async def delete(request: Request):
    proxy = request.query_params.get('proxy')
    _status = proxy_handler.delete(Proxy(proxy))
    data = _status
    return success(data=data)


@app.get('/count')
async def count():
    proxies = proxy_handler.get_all()
    http_type_dict = {}
    source_dict = {}
    for proxy in proxies:
        http_type = 'https' if proxy.https else 'http'
        http_type_dict[http_type] = http_type_dict.get(http_type, 0) + 1
        for source in proxy.source.split('/'):
            source_dict[source] = source_dict.get(source, 0) + 1
    data = {"http_type": http_type_dict, "source": source_dict, "count": len(proxies)}
    return success(data=data)


@app.get('/agents')
async def agents(request: Request):
    https = request.method.lower() == 'https'
    proxies = proxy_handler.get_all(https)
    return templates.TemplateResponse('agents.html', {"request": request, "data": proxies})
    # print(type(proxies))


def run_fastapi():
    uvicorn.run('api.api:app', host=conf.server_host, port=conf.server_port, reload=True)


def success(*, data: Union[list, dict, str]) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'message': 'Success',
            'data': data,
        }
    )


def error(*, data: str = None, message: str = 'BAD REQUEST') -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'message': message,
            'date': data,
        }
    )


if __name__ == '__main__':
    run_fastapi()
