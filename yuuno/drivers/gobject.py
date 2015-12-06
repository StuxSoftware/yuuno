#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from gi.repository import Pango, PangoCairo

from yuuno.environment import TextExtent
from yuuno.parser import Style

# Pango already does the scaling for us, so we don't have to do anything.
SCALE = Pango.SCALE

class _TextExtents(object):
    """
    Calculates the text extents using the GLib Pango library.
    It relies on the FontConfig Font Map defined in PangoCairo.
    """

    def __init__(self):
        self.context = Pango.Context()
        self.context.set_font_map(PangoCairo.FcFontMap())

    def __call__(self, string, style):
        fd = Pango.FontDescription()

        fd.set_family(style.fontname)
        if style.bold > 1:
            fd.set_weight(style.bold)
        elif style.bold <= 0:
            fd.set_weight(Pango.Weight.NORMAL)
        else:
            fd.set_weight(Pango.Weight.BOLD)

        if style.italic > 1:
            fd.set_style(style.italic)
        elif style.italic <= 0:
            fd.set_style(Pango.Style.NORMAL)
        else:
            fd.set_style(Pango.Style.ITALIC)

        fd.set_size(style.fontsize*SCALE)

        self.context.set_font_description(fd)

        # Pango does not support external leading.
        metrics = self.context.get_metrics()
        res_desc = metrics.get_descent()/SCALE
        res_extlead = 0

        # Now we determine the height of the layout.
        layout = Pango.Layout(self.context)
        layout.set_text(string, len(string))
        size = layout.get_pixel_size()
        res_width, res_height = size

        return TextExtent(res_width, res_height, res_desc, res_extlead)

textextents = _TextExtents()
