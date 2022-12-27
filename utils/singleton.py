#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'

from typing import Any


class Singleton(type):
    """
    Singleton Metaclass
    """

    _instance = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args)
        return cls._instance[cls]
