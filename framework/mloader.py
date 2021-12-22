#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module loader
    ~~~~~~~~~~~~~
    program that loads modules and executes them.
    It is responsible for the following tasks:
        - loading modules
        - executing modules
        - managing the modules current active memory (short term memory)
            like tasks, events, and other data.
"""


import os
from importlib.machinery import SourceFileLoader
from pathlib import Path

from logger import get_logger
import crud

lgr = get_logger(__name__)

class loader(crud.database):

    def __init__(self, path: str):
        self.path = os.path.join(Path(__file__).parent, path)
        self.files = []
        self.modules = {}

    def load(self) -> object:
        self.get_modules()
        
        if self.files:
            for path, name in self.files:
                mm = SourceFileLoader(name, path).load_module()
                try:
                    main = getattr(mm, name)
                    self.modules[name] = main
                except AttributeError as e:
                    lgr.warning("Module {} can't be found. {}".format(name, e))

            lgr.info("{} module(s) loaded.".format(len(self.modules)))

        return self

    def start(self):
        if self.modules:
            for name in self.modules.keys():
                self.modules[name] = self.modules[name]()

    def get_modules(self) -> None:
        self.files = []
        self.modules = {}
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".py"):
                    self.files.append([os.path.join(root, file), file.split(".")[0]])

    def get_files(self) -> list:
        return self.files

    def get_path(self) -> str:
        return self.path

if __name__ == '__main__':
    l = loader('modules')
    print(l.load())
