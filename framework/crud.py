#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains the CRUD operations for the database.
    actions:
        - create
        - read
        - update
        - delete

    author: @leogaddd

"""

from logger import get_logger
import os
from pathlib import Path
import sqlite3

lgr = get_logger(__name__)

class database:

    def __init__(self, db_path: str) -> None:
        self.db_path = os.path.join(Path(__file__).parent, db_path)

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            lgr.error("Error connecting to database: {}".format(e))

    def close(self):
        self.conn.close()