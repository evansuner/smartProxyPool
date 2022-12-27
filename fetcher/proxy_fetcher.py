#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import re
import json
from datetime import datetime
from time import sleep
from utils.web_request import WebRequest
from urllib import parse
from urllib3.exceptions import InsecureRequestWarning
import requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ProxyFetcher:
    """proxy getter"""

    @classmethod
    def free_proxy01(cls):
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        start_url = "https://www.zdaye.com/dayProxy.html"
        html_tree = WebRequest().get(start_url).tree
        latest_page_time = html_tree.xpath("//span[@class='thread_time_info']/text()")[0].strip()
        from datetime import datetime
        interval = datetime.now() - datetime.strptime(latest_page_time, "%Y/%m/%d %H:%M:%S")
        if interval.seconds < 300:  # 只采集5分钟内的更新
            target_url = "https://www.zdaye.com/" + html_tree.xpath("//h3[@class='thread_title']/a/@href")[0].strip()
            while target_url:
                _tree = WebRequest().get(target_url).tree
                for tr in _tree.xpath("//table//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield f'{ip}:{port}'
                next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
                target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False
                sleep(5)

    @classmethod
    def free_proxy02(cls):
        """
        http://www.66ip.cn
        """
        url = "http://www.66ip.cn/"
        resp = WebRequest().get(url, timeout=10).tree
        for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
            if i > 0:
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield f"{ip}:{port}"

    @classmethod
    def free_proxy03(cls):
        """
        开心代理
        """
        urls = [
            'http://www.kxdaili.com/dailiip/1/1.html',
            'http://www.kxdaili.com/dailiip/1/2.html',
            'http://www.kxdaili.com/dailiip/1/3.html',
        ]
        for url in urls:
            tree = WebRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield f"{ip}:{port}"

    @classmethod
    def free_proxy04(cls):
        """
        FreeProxyList https://www.freeproxylists.net/zh/
        """
        url = "https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=90"
        tree = WebRequest().get(url).tree

        def parse_ip(input_str):
            html_str = parse.unquote(input_str)
            regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            ips = re.findall(regex, html_str)
            return ips[0] if ips else None

        for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
            ip = parse_ip("".join(tr.xpath('./td[1]/script/text()')).strip())
            port = "".join(tr.xpath('./td[2]/text()')).strip()
            if ip:
                yield f'{ip}:{port}'

    @classmethod
    def free_proxy05(cls, page_count=3):
        """
        https://www.kuaidaili.com
        """
        url_patterns = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/',
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_patterns:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @classmethod
    def free_proxy06(cls):
        """ FateZero http://proxylist.fatezero.org/ """
        url = "http://proxylist.fatezero.org/proxy.list"
        try:
            resp_text = WebRequest().get(url).text
            for each in resp_text.split("\n"):
                json_info = json.loads(each)
                if json_info.get("country") == "CN":
                    yield f"{json_info.get('host', '')}:{json_info.get('port', '')}"
        except Exception as e:
            pass

    @classmethod
    def free_proxy07(cls):
        """
        http://www.ip3366.net
        """
        urls = [
            'http://www.ip3366.net/free/?stype=1',
            "http://www.ip3366.net/free/?stype=2",
        ]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            regex = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>'
            proxies = re.findall(regex, r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    # @classmethod
    # def free_proxy08(cls):
    #     """
    #     小幻代理
    #     """
    #     urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
    #     for url in urls:
    #         r = WebRequest().get(url, timeout=10)
    #         regex = r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>'
    #         proxies = re.findall(regex, r.text)
    #         for proxy in proxies:
    #             yield ":".join(proxy)

    @classmethod
    def free_proxy09(cls, page_count=1):
        """
        https://ip.jiangxianli.com/?page=1&country=中国
        """
        for i in range(1, page_count + 1):
            url = 'https://ip.jiangxianli.com/?page={}&country=中国'.format(i)
            tree = WebRequest().get(url, verify=False).tree
            for index, tr in enumerate(tree.xpath('//table//tr')):
                if index == 0:
                    continue
                try:
                    ip = tr.xpath('./td[1]/text()')[0].strip()
                    port = tr.xpath('./td[2]/text()')[0].strip()
                except Exception as e:
                    continue
                if port and ip:
                    yield f'{ip}:{port}'

    @classmethod
    def free_proxy10(cls):
        """89免费代理"""
        resp = WebRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        tree = resp.tree
        trs = tree.xpath('//div[3]/div[1]/div/div[1]/table//tr')
        for i in range(1, len(trs)):
            ip = tree.xpath(f'//div[3]/div[1]/div/div[1]/table//tr[{i}]/td[1]/text()')[0].strip()
            port = tree.xpath(f'//div[3]/div[1]/div/div[1]/table//tr[{i}]/td[2]/text()')[0].strip()
            yield f'{ip}:{port}'


if __name__ == '__main__':
    p = ProxyFetcher()
    # p.free_proxy09()
    for _ in p.free_proxy01():
        print(_)
