#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

import json


class Proxy:
    def __init__(self, proxy, fail_count=0, region='', anonymous='',
                 source='', check_count=0, last_status='',
                 last_time='', https=False) -> None:
        self._proxy = proxy
        self._fail_count = fail_count
        self._region = region
        self._anonymous = anonymous
        self._source = source.split('/')
        self._check_count = check_count
        self._last_status = last_status
        self._last_time = last_time
        self._https = https

    @classmethod
    def create_from_json(cls, proxy_json: json):
        _dict = json.loads(proxy_json)
        return cls(
            proxy=_dict.get('proxy', ''),
            fail_count=_dict.get('fail_count', ''),
            region=_dict.get('region', ''),
            anonymous=_dict.get('anonymous', ''),
            source=_dict.get('source', ''),
            check_count=_dict.get('check_count', 0),
            last_status=_dict.get('last_status', ''),
            last_time=_dict.get('last_time', ''),
            https=_dict.get('https', False),
        )

    @property
    def proxy(self):
        """
        代理 ip:port
        """
        return self._proxy

    @property
    def fail_count(self):
        """
        检测失败次数
        """
        return self._fail_count

    @property
    def region(self):
        """
        地理位置(国家/城市)
        """
        return self._region

    @property
    def anonymous(self):
        """
        匿名
        """
        return self._anonymous

    @property
    def source(self):
        """
        代理来源
        """
        return '/'.join(self._source)

    @property
    def check_count(self):
        """
        代理检测次数
        """
        return self._check_count

    @property
    def last_status(self):
        """
        最后一次检测结果, True为可用; False为不可用
        """
        return self._last_status

    @property
    def last_time(self):
        """
        最后一次检测时间
        """
        return self._last_time

    @property
    def https(self):
        """
        是否支持https
        """
        return self._https

    @property
    def to_dict(self):
        """python对象格式数据"""
        return {
            'proxy': self.proxy,
            'fail_count': self.fail_count,
            'region': self.region,
            'anonymous': self.anonymous,
            'source': self.source,
            'check_count': self.check_count,
            'last_status': self.last_status,
            'last_time': self.last_time,
            'https': self.https,
        }

    @property
    def to_json(self):
        """json格式数据"""
        return json.dumps(self.to_dict, ensure_ascii=False)

    @fail_count.setter
    def fail_count(self, value):
        self._fail_count = value

    @check_count.setter
    def check_count(self, value):
        self._check_count = value

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @last_time.setter
    def last_time(self, value):
        self._last_time = value

    @region.setter
    def region(self, value):
        self._region = value

    @https.setter
    def https(self, value):
        self._https = value

    @source.setter
    def source(self, source_str):
        if source_str:
            self._source.append(source_str)
            self._source = list(set(self._source))

    def add_source(self, source_str):
        if source_str:
            self._source.append(source_str)
            self._source = list(set(self._source))