#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from gi.repository import Pango, PangoCairo

from yuuno.environment import TextExtent
from yuuno.parser import Style

class _TextExtents(object):

    def __init__(self):
        self.context = Pango.Context()
        self.context.set_font_map(PangoCairo.FcFontMap())

    def __call__(self, string, style):
        pass
