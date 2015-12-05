
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
import io
import os, sys

import docopt

from yuuno.parser import Dialogue, Document
from yuuno.environment import Environment
from yuuno.templater import Templater


PROGNAME=os.path.dirname(sys.argv[0])


class DefaultEnvironment(Environment):

    def __init__(self):
        self.logfile = io.StringIO()
        self.output = None
        self.input = None
        self._init = False

    def log(self, message: str) -> None:
        """
        Log the message.
        """
        print(message, file=self.logfile)

    def main(self, parser: Templater) -> None:
        """
YuunoFX Script.

Usage:
    %(fn)s [options] timing

Options
   -l,--log     [Default:*stderr]
   -o,--output  [Default:-]

        """
        if self._init:
            raise RuntimeError("Environment already initialized.")

        def _parse_input(data, min_default=None, mode="r"):
            if data == "-":
                return open(min_default, mode)
            elif data == "*stderr":
                return sys.stderr
            elif data == "*stdin":
                return sys.stdin
            elif data == "*stdout":
                return sys.stdout
            elif data == "*null":
                return open(os.devnull, mode)
            else:
                return open(data, mode)

        # Parse options.
        result = docopt.docopt(self.main.__doc__%{'fn':PROGNAME})

        # Store the logdata.
        logdata = self.logfile.getvalue()

        # Initialize the environment.
        self.input = Document.parse_file(
                _parse_input(result["timings"], sys.stdin, "r")
        )
        self.logfile = _parse_input(result["--log"], sys.stderr, "w")
        self.output = Document()
        self._init = True

        # Copy logfile output.
        self.logfile.write(logdata)
        self.logfile.flush()

        # Run the actual script.
        parser.run()

        # Write document.
        self.output.dump_file(_parse_input(result["--output"], sys.stdout, "w"))

    def get_data(self, file):
        if file is None:
            return self.input
        return Document.parse_file(open(file, f))

    def dump(self, line):
        self.output.events.append(line)
