# SmartProxyPool crawler agent pool

## Run Project
### Local Running
+ git clone
```bash
git clone git@github.com:evansuner/smartProxyPool.git
```

+ Install requirements
```bash
pip3 install -r requirements.txt
```
+ Update Configuration(option)  
`setting.py`
```python
# API Server Configuration
HOST = "0.0.0.0"               # IP
PORT = 9091                    # Listen port

# Database Configuration
DB_CONN = 'redis://:pwd@127.0.0.1:8888/0'

# ProxyFetcher Configuration
PROXY_FETCHER = [
    "freeProxy01",      # Here is the enabled proxy fetching method name,
    "freeProxy02",      # All fetch methods located in fetcher/proxyFetcher.py
    # ....
]
```
+  Start project
```bash
# If you already have the running conditions, you can start it through server_proxy_pool.py。
# The program is divided into: schedule scheduler and server Api service

# start schedule programme and web api server
python3 server_proxy_pool.py schedule &
python3 server_proxy_pool.py server

```
### Docker Running
```bash
docker pull jhao104/proxy_pool

docker run --env DB_CONN=redis://:123456@ip:port/0 -p 9090:9090 jhao104/proxy_pool:latest
```
### Docker Compose Running
```bash
docker compose up -d
```

## Usage
+ Api
start server,  http://127.0.0.1:9090:

| api      | 	method	 | Description              | 	params                                                       |
|:---------|:---------|:-------------------------|:--------------------------------------------------------------|
| /        | 	GET     | 	api介绍	                  | None                                                          |
| /get     | 	GET     | 	randomly get an agent   | 	option params: ?type=https filter type is https              |
| /pop     | GET	     | get and remove an agent	 | option params: ?type=https filter type is https               |
| /all	    | GET	     | get all agents	          | option params: ?type=https filter type is https               |
| /count	  | GET	     | view counts of agents	   | None                                                          |
| /delete	 | GET	     | delete agent	            | ?proxy=host:ip                                                |

+ Using in Spiders  
If these proxies are used in spiders, these APIs need to be wrapped into function calls, example:
```python
import requests

def get_proxy():
    return requests.get('https://127.0.0.1:9090/get/').json()
def delete_proxy(proxy):
    return requests.get(f'https://127.0.0.1:9090/delete?proxy={proxy}')

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
    def freeProxyCustom1():
        """the function name should not duplicate exist"""
        proxies = ['x.x.x.x:5000','x.x.x.x:5001']
        for proxy in proxies:
            yield proxy
```
2. update settings config:
```python
PROXY_FETCHER = [
    ...,
    'freeProxyCustom1'
]
```
Finally, `schedule` process would use your method to scrapy new proxies.