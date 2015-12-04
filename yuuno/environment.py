#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from typing import AnyStr, Optional

from yuuno.parser import Document, Dialogue


class Environment(object):
    """
    Base-Class for environment.
    """

    def main(self, environment) -> None:
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


_environment = None
def set_environment(environment):
    global _environment
    _environment = environment

def get_environment():
    return _environment