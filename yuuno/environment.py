#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
import collections
from typing import AnyStr, Optional, List, Callable

from yuuno.namespace import Namespace
from yuuno.parser import Document, Dialogue, Style


TextExtent = collections.namedtuple("TextExtent", "width height descent extlead")


class Environment(object):
    """
    Base-Class for environment.
    """

    def log(self, message) -> None:
        """
        Log the given message.
        """

    def main(self, parser) -> None:
        """
        Represents the main function for this environment. It is a callback
        to signal the script that the script is ready for rendering.
        """
        pass

    def get_data(self, file: Optional[AnyStr]=None) -> Document:
        """
        Returns the raw data of the timing file for the karaoke fx.
        :param file: The file to read. Defaults to the main timing file passed to the environment.
        :return: A raw data object. Returns an empty result if the file can't be loaded by the environment.
        """
        return None

    def dump(self, line: Dialogue) -> None:
        """
        Dumps the given line into the file.
        :param line: The line to dump
        """
        pass

    def get_processors(self) -> List[Callable[[Document, Namespace], None]]:
        """
        Returns the default processors of this environment.
        """
        return []

    def text_extents(self, string: AnyStr, style: Style) -> TextExtent:
        """
        Returns the text extents.
        """
        return TextExtents(0, 0, 0, 0)

_environment = None
def set_environment(environment):
    global _environment
    _environment = environment

def get_environment():
    return _environment
