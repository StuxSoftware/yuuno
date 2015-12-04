#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""

import re
from collections import namedtuple

import yuuno.parser as document


class Time(namedtuple("BaseTime", "start end")):
    __slots__ = ()

    @property
    def duration(self):
        return self.end - self.end

    def retime(self, *, start: int=0, end: int=0) -> object:
        """
        Retimes the time relative to the given time object.
        """
        return self.__class__(self.start - start, self.end - end)

    def shift(self, delta: int) -> object:
        """
        Shifts the time.
        """
        return self.retime(start=delta, end=delta)


Margins = namedtuple("Margins", "l r v")
Line = namedtuple("Line", "style margins time actor effect line")


class Document(object):
    """
    Parser for the document.
    """

    def __init__(self, fp=None):
        if fp is not None:
            self.styles, self.lines = self.loadfile(fp)
        else:
            self.styles = []
            self.lines = []

    def dumpfile(self, fp) -> None:
        """
        The dumped file.
        """

        wdoc = document.Document()
        wdoc.styles = self.styles[:]
        wdoc.events = [
            document.Dialogue()
        ]

    @staticmethod
    def loadfile(fp: open) -> (document.Style, Line):
        cdoc = document.Document.parse_file(fp)

        lines = []
        for event in cdoc.events:
            if not isinstance(event, document.Dialogue):
                continue
            line = Line(
                style=event.style,
                margins=Document.parse_magins(event),
                time=Time(event.start, event.end),
                actor=event.name,
                effect=event.effect,
                line=event.text
            )
            lines.append(line)

        return cdoc.styles, lines

    @staticmethod
    def parse_magins(event: document.Dialogue) -> Margins:
        """
        Parses the margins
        :param event:  The event
        :return:       The margins
        """
        def _decide_source(
                event: document.Dialogue, style: document.Style,
                type: str
        ) -> int:
            # Decide from which source we should get our margins.
            evt_m = getattr(event, "margin_" + type)
            if evt_m == 0:
                return getattr(style, "margin_" + type)
            return evt_m

        return Margins(
            **{t: _decide_source(event, event.style, t) for t in "lrv"}
        )


class Syllable(namedtuple("BaseSyllable", "time line text")):
    """
    Represents a single syllable.
    """

    # The regex that will match correctly formatted syllable lines.
    SYLLABLE_REGEX = re.compile(r"\{\\[Kk][of]?(\d+)}([^{]*)")

    @classmethod
    def parse_line(cls, line: Line):
        """
        Parses the line.
        :param line:   The line that should be parsed.
        :return:       A generator for all syllables.
        """
        cur_time = line.time.start*10
        for match in cls.SYLLABLE_REGEX.finditer(line.line):
            dur, text = match.groups()
            end_time = cur_time + dur
            yield cls(Time(cur_time, end_time), line, text)
            cur_time = end_time