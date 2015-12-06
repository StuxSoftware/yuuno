#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from yuuno.processing.core import DocumentParser
from yuuno.environment import get_environment, Environment
from yuuno.namespace import Namespace

class Templater(object):
    """
    The yuuno templater object.
    """

    def __init__(self, environment: Environment=None):
        if environment is None:
            environment = get_environment()
        self.environment = environment
        self.root = Namespace()
        self.functions = []
        self._processors = None
        self.parser = DocumentParser()

    @property
    def processors(self):
        if self._processors is None:
            self._processors = self.environment.get_processors()
        return self._processors

    @processors.fset
    def processors(self, value):
        self._processors = value

    @processors.fdel
    def processors(self, value):
        self._processors = None

    def register(self, func):
        self.functions.append(func)
        return func

    def _call(self, func, ns):
        yield from (line.eval_line(ns) for line in func(ns))

    def load(self, namespace, name=None, file=None):
        """
        Loads a file into the namespace.

        :param namespace: The namespace.
        :param name:      The internal id
        """
        if name is not None:
            setattr(namespace, name, Namespace())
            namespace = getattr(namespace, name)

        doc = self.environment.get_data(file)
        self.parser.on_new_document(namespace, doc)

    def run(self):
        ns = Namespace(self.root)
        ns.parser = self

        self.load(ns, name=None, file=None)

        for function in functions:
            for line in function(ns):
                self.environment.dump(line)

        del ns.parser

