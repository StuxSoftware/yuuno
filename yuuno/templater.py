#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from yuuno.environment import get_environment
from yuuno.namespace import Namespace

class Templater(object):
    """
    The yuuno templater object.
    """

    def __init__(self, environment=None):
        self.environment = get_environment() if environment is None else environment
        self.root = Namespace()
        self.functions = []

    def register(self, func):
        self.functions.append(func)
