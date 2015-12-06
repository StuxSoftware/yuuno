#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from yuuno.processing.core import Processor


class ConceptProcessor(self):
    """
    The basic concept processor that handles the size processing
    for new text concepts of the processor.

    Each concepts namespace has these attributes:
    - text       - The text that should be measured
    - style      - The style of the text
    - type       - The type of the concept.

    And optionally
    - pre_text   - The text of the line before the text of the
                   concept itself.
                   [Default: empty string]
    - containers - This is a list of concepts that contain this
                   concept.
    - start      - The start time of the text.
    - end        - The end time of the text.
    - i          - The index
    - list       - The list of all instances of the concept.
    """

    @classmethod
    def get_dependencies(cls):
        return []

    def init(self, templater, parser):
        # on_concept(Namespace)
        self.on_concept = parser.create_event("concept")
