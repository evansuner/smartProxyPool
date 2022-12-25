#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from typing import Any


class Singleton(type):
    """
    Singleton Metaclass
    """

    _instance = {}

    def __call__(self, *args: Any, **kwsds: Any) -> Any:
        if self not in self._instance:
            self._instance[self] = super(Singleton, self).__call__(*args)
        return self._instance[self]