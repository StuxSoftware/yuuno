#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
from yuuno.processing.core import Processor
from yuuno.processing.concept import ConceptProcessor


class DocumentProcessor(Processor):
    """
    The document processor sets the global style database and the
    metadata database.
    """

    def init(self, templater, parser):
        self.parser.on_new_document += self.handle_new_document

    def handle_new_document(self, ns, document):
        # Set the styles of the new document.
        ns['styles'] = {
            style.name: style
            for style in document.styles
        }

        # Set the metadata on the document.
        ns['meta'] = Namespace()
        for k,v in document.fields.items():
            ns['meta'][k] = v


class LineProcessor(Processor):

    @classmethod
    def get_dependencies(cls):
        return [ConceptProcessor, DocumentProcessor]

    def init(self, templater, parser):
        self.parser = parser
        self.parser.on_new_document += self.list_lines
        self.handle_concept = self.parser.on_concept

    def list_lines(cls, ns, document):
        ns['lines'] = lines = list()

        index = 0
        for event in document.events:
            if not isinstance(event, Dialogue):
                continue

            # Create the new line namespace.
            linens = Namespace()
            lines.append(linens)

            # Initialize the line namespace.
            linens['type'] = "line"
            linens['start'] = int(event.start)
            linens['end'] = int(event.end)
            linens['style'] = ns.styles[event.style]
            linens['containers'] = []
            linens['pre_text'] = ""
            linens['list'] = lines
            linens['i'] = index

            self.handle_concept(ns)

            index += 1


class SyllableProcessor(Processor):

    @classmethod
    def get_dependencies(cls):
        return [ConceptProcessor, LineProcessor]

    def init(self, templater, parser):
        self.parser = parser
        self.parser.on_concept += self.list_syllables
        self.handle_concept = self.parser.on_concept

    def list_syllables(self, ns):
        # We only handle line templates.
        if ns.type != "line":
            return


