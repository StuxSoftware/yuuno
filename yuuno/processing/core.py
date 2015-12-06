#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yuuno FX.

Taking KaraTemplater to it's logical conclusion.
"""
import collections
import toposort
from yuuno.environment import get_environment


class Processor(object):
    """
    Loads the required processors.
    """

    def __init__(self):
        pass

    @classmethod
    def get_dependencies(cls):
        return []

    def init(self, templater, parser):
        pass


class DocumentParser(object):
    """
    Creates a new document.
    """

    def __init__(self, parser):
        self.parser = parser
        self.manager = EventManager()
        self.processors = {}
        # on_new_document(Namespace, Document)
        self.on_new_document = self.manager.create("new_document")

    def get_processor(self, cls):
        return self.processors[cls]

    def create_event(self, name):
        event = self.manager.create(name)
        setattr(self, "on_"+name, event)
        return event

    def init_processors(self):
        dep_graph = {p:p.get_dependencies() for p in self.parser.processors}
        for processor in toposort_flatten(dep_graph):
            processor_inst = processor()
            self.processors[processor] = processor_inst
            processor_inst.init(self.parser, self)

    def process_document(self, namespace, document):
        self.on_new_document(namespace, document)


class Event(object):
    """
    Represents a new event
    """

    def __init__(self, manager, name):
        self.manager = manager
        self.name = name

    def __call__(self, *args, **kwargs):
        self.manager.emit(self.name, *args, **kwargs)

    def register(self, handler):
        self.manager.register(self.name, handler)
        return self
    __iadd__ = register


class EventManager(object):
    """
    A simple event manager.

    It is used to allow processors to register event handlers for new concept.
    It allows more pluggable processors for text.

    Each new processor registers its events and emits other ones so other
    events can handle updates.
    """

    def __init__(self):
        self.handlers = collections.defaultdict(list)

    def create(self, name):
        self.emit("new_event", name)
        return Event(self, name)

    def emit(self, name, *args, **kwargs):
        for handler in self.handlers[name]:
            handler(name, *args, **kwargs)

    def register(self, name, handler):
        self.handlers[name].append(handler)
