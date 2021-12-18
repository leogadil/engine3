#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Personal Assistant Engine
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    serves as the main engine of the Personal Assistant.
    It is responsible for the following tasks:
        - loading the configuration file 
        - loading the modules
        - loading the plugins
        - loading the commands
        - loading the triggers
"""

import abc

class engine:

    def __init__(self, child) -> None:
        self.child = child
        self.commands = {
            "help": self.help,
        }
    
    @abc.abstractmethod
    def prepare(self) -> None:
        pass


if __name__ == '__main__':
    e = engine()