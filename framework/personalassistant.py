#!/usr/bin/env python
# -*- coding: utf-8 -*-


version = "0.0.1"

"""
    Personal Assistant Engine
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    serves as the main engine of the AI.
    It is responsible for the main loop of the application.
    
    It is responsible for the following tasks:
        - loading the configuration file 
        - loading the modules
        - loading the plugins
        - loading the commands
        - loading the triggers
"""

import abc
from logger import get_logger
from time import sleep
import activememory

lgr = get_logger(__name__)

class engine:

    def __init__(self, child: object = None,
                    override_command: bool = False,
                    override_intent_model: bool = False) -> None:

        self.override_command = override_command
        self.override_intent_model = override_intent_model
        self.running = False
        self.num_worker = 1
        self.name = "Personal Assistant"
        self.version = version

        if child is not None:
            self.child = child
    
    @abc.abstractmethod
    def prepare(self) -> None:
        lgr.warning("No External Preparation Steps Found.")

    def initialize(self):
        self.prepare()
        self.running = True

    def run(self) -> None:
        lgr.info("Loading initiatives...")
        self.main_thread()
    
    def main_thread(self) -> None:
        try:
            lgr.info(f"{self.name} is ready to serve you.")
            while self.running:
                # do the main loop here
                sleep(.1)
        except KeyboardInterrupt:
            self.running = False
            lgr.info("Shutting Down...")
            
            

if __name__ == '__main__':
    e = engine()
    e.initialize()
