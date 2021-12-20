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

import sqlite3

class database:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        
        self.cursor = self.conn.cursor()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)

    def close(self):
        self.conn.close()