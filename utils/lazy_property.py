#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Evan'


class LazyProperty():
    """
    LazyProperty
    """

    def __init__(self, func) -> None:
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            return value
