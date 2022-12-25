## smartProxyPool爬虫代理池
### 运行项目
#### Download code
+ git clone
```bash
git clone git@github.com:evansuner/smartProxyPool.git
```
+ releases
```bash

```
#### Install requirements
```bash
pip3 install -r requirements.txt
```
#### Update config(option)
```bash
# setting.py 为项目配置文件

# 配置API服务

HOST = "0.0.0.0"               # IP
PORT = 5000                    # 监听端口


# 配置数据库

DB_CONN = 'redis://:pwd@127.0.0.1:8888/0'


# 配置 ProxyFetcher

PROXY_FETCHER = [
    "freeProxy01",      # 这里是启用的代理抓取方法名，所有fetch方法位于fetcher/proxyFetcher.py
    "freeProxy02",
    # ....
]
```
#### Start project
```bash
# 如果已经具备运行条件, 可用通过proxyPool.py启动。
# 程序分为: schedule 调度程序 和 server Api服务

# 启动调度程序
python proxyPool.py schedule

# 启动webApi服务
python proxyPool.py server
```
### Docker Image
```bash
docker pull jhao104/proxy_pool

docker run --env DB_CONN=redis://:password@ip:port/0 -p 5010:5010 jhao104/proxy_pool:latest
```
### Docker compose
```bash
docker compose up -d
```

## Usage
+ Api
启动web服务后, 默认配置下会开启 http://127.0.0.1:5010 的api接口服务:

| api      | 	method	 | Description | 	params                         |
|:---------|:---------|:------------|:--------------------------------|
| /        | 	GET     | 	api介绍	     | None                            |
| /get     | 	GET     | 	随机获取一个代理   | 	可选参数: ?type=https 过滤支持https的代理 |
| /pop     | GET	     | 获取并删除一个代理	  | 可选参数: ?type=https 过滤支持https的代理  |
| /all	    | GET	     | 获取所有代理	     | 可选参数: ?type=https 过滤支持https的代理  |
| /count	  | GET	     | 查看代理数量	     | None                            |
| /delete	 | GET	     | 删除代理	       | ?proxy=host:ip                  |

+ Using in Spiders
If these proxies will use in spiders, these APIs need to be wrapped into function calls, example:
```python
import requests

def get_proxy():
    return requests.get('https://127.0.0.1:5010/get/').json()
def delete_proxy(proxy):
    return requests.get(f'https://127.0.0.1:5010/delete?proxy={proxy}')

# your spider code here
def parse():
    """..."""
    retry_count = 5
    proxy = get_proxy().get('proxy')
    while retry_count > 0:
        try:
            content = requests.get('https://www.example.com', proxies={'http':f'http://{proxy}'})
            return content
        except TimeoutError:
            retry_count -= 1
    delete_proxy(proxy)
    return None
```
### Self Configuration for proxy
Although this project provides several free proxy repositories, the quality of free proxies is limited, if the proxies you get from this project are not useful, here provides you a method to add new proxy repos:
1. add a new staticmethod in class `ProxyFetcher`, this function should use generator(yield) returns a formatted proxy like`host:ip`, for example:
```python
class ProxyFetcher:
    """..."""
    ...
    @staticmethod
    def free_proxy_custom1():
        """the function name should not duplicate exist"""
        proxies = ['x.x.x.x:5000','x.x.x.x:5001']
        for proxy in proxies:
            yield proxy
```
2. update settings config:
```python
PROXY_FETCHER = [
...,
'free_proxy_custom1'
]
```
finally, `schedule` process would use your method to scrapy new proxies.