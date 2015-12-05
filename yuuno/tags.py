#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from datetime import import timedelta
from yuuno.parser import Dialogue


class BaseTag(object):
    """
    Implements a base tag.
    """

    def evaluate(self, namespace):
        pass

    def __call__(self, namespace):
        return self.evaluate(namespace)

class TagContainer(BaseTag):
    """
    Returns a container for base tags.
    """

    def __init__(self, tags=()):
        self.tags = tags

    def __add__(self, other):
        return self.__class__(tags=self.tags+(other,), **self._get_data())

    def _get_data(self):
        return {}

    def evaluate(self, namespace):
        return "".join(tag.evaluate(namespace) for tag in self.tags)


class Text(BaseTag):

    def __init__(self, text=""):
        self.text = text

    def evaluate(self, namespace):
        text = self.text
        if callable(text):
            text = text(namespace)
        return text


class SimpleTag(BaseTag):
    """
    A simple tag.
    """
    name = None

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return ContainerTag((self, other))

    def evaluate(self, namepace):
        val = self.value

        # Evaluate callables.
        if callable(val):
            val = val(namespace)

        # Evaluate multi value things.
        if not isinstance(val, str):
            res = []
            in_comment = False
            for v in val:
                if isinstance(v, Text):
                    if in_comment:
                        res.append("}")
                    res.append(v.evaluate(namespace))
                elif isinstance(v, Tag):
                    if not in_comment:
                        res.append("{")
                    res.append(v.evaluate(namespace))
                elif callable(v):
                    res.append(v(namespace))
                else:
                    res.append(str(v))
            if in_comment:
                res.append("}")
            val = "".join(res)

        if isinstance(val, BaseTag):
            val = "(%s)"%(val.evaluate(namespace))

        return "\\%s%s"%(self.name, val)

    @classmethod
    def new(cls, name, short):
        return type(name, (cls,), {"name":short})


class Line(ContainerTag):
    def __init__(self, start=0, end=0, layer=0, style="Default"):
        super(Line, self).__init__()
        self.start = start
        self.end = end
        self.layer = layer
        self.style = style

    def _get_data(self):
        return {
            "start": self.start,
            "end": self.end,
            "layer": self.layer,
            "style": self.style
        }

    def to_dialogue(self, namespace):
        result = Dialogue()
        result.start = timedelta(ms=self.start)
        result.end = timedelta(ms=self.end)
        result.style = self.style
        result.layer = layer
        result.text = self.evaluate(namespace)
        return result

    def eval_line(self, namespace):
        result = Text(self.evaluate(namespace))
        line = self + Text()
        line.value = (result,)
        return line
