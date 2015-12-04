#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
import typing
_DUMMY = []

class Namespace(object):
    """
    A namespace for the function calls.
    """

    __slots__ = ("scope", "parent")

    def __init__(self, parent=None):
        self.scope = {}
        self.parent = parent

    def _eval_passdown(self, passdown:bool):
        if self.parent is None:
            return False
        return passdown

    def _get(self, name: str, d: typing.Any=_DUMMY, *, passdown: bool=True):
        passdown = self._eval_passdown(passdown)
        if name not in self.scope:
            if passdown:
                return self.parent._get(name, d)
            if d is _DUMMY:
                raise KeyError(name)
            return d
        return self.scope.get(name)

    def _set(self, name:str, value: typing.Any, *, passdown: bool=True):
        passdown = self._eval_passdown(passdown)
        if passdown and name in self.parent:
            self.parent._set(name, value)
            return
        self.scope[name] = value

    def _del(self, name:str, *, passdown: bool=True):
        passdown = self._eval_passdown(passdown)
        if self._has(name, passdown=False):
            del self.scope[name]

        if passdown:
            self.parent._del(name, passdown=True)

    def _has(self, name: str, *, passdown: bool = True):
        passdown = self._eval_passdown(passdown)
        if name in self.scope:
            return True
        if passdown and self.parent._has(name, passdown=True):
            return True
        return False

    def get(self, name: str, d: typing.Any=_DUMMY):
        return self._get(name, d, passdown=True)

    def __getitem__(self, item):
        return self._get(item, passdown=False)

    def __setitem__(self, item, value):
        self._set(item, value, passdown=False)

    def __delitem__(self, item):
        self._del(item, passdown=False)

    def __getattr__(self, attr):
        return self._get(attr, passdown=True)

    def __contains__(self, item):
        return self._has(item, passdown=True)

    def __setattr__(self, attr, value):
        if attr in Namespace.__slots__:
            super(Namespace, self).__setattr__(attr, value)
        else:
            self._set(attr, value, passdown=True)

    def __delattr__(self, attr):
        if attr in Namespace.__slots__:
            raise AttributeError("Read Only attribute.")
        self._del(attr)

