#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Active Memory
    ~~~~~~~~~~~~~
    program that serves the short term memory of the AI.
    It is responsible for the following tasks:
        - managing the programs current active memory (short term memory)
            like tasks, events, and other data.
        
"""
import os
import sqlite3
import sys
from traceback import format_exc

import crud
from logger import get_logger

lgr = get_logger(__name__)

class activememory():

    def __init__(self) -> None:
        # create active memory subfolder if it does not exist

        folder = 'framework/activememory'
        if not os.path.exists(folder):
            lgr.warning(f'Creating folder: {folder}')
            os.makedirs(folder)

        self.task = None

    def init_task(self):
        self.task = taskactivememory('activememory/task_memory.db')


class taskactivememory(crud.database):

    def __init__(self, db_path: str) -> None:
        super().__init__(db_path)
        self.create_task_memory()

    def create_task_memory(self) -> None:
        self.connect()
        """
        create a database table for tasks queue
        """

        task_memory_query = '''
            CREATE TABLE IF NOT EXISTS task_queue(
                id STRING PRIMARY KEY,
                query STRING,
                status STRING
            )
        '''

        try:
            self.cursor.execute(task_memory_query)
            self.conn.commit()
            self.close()
        except sqlite3.OperationalError as e:
            lgr.error("Error creating task_queue table: {}".format(e))
            # traceback = format_exc()
            # lgr.error("{}".format(traceback))
            sys.exit(1)

    def push_task(self, _query) -> None:
        self.connect()

        push_task_query = '''
            INSERT INTO task_queue(id, query, status) values(?,?,?)
        '''

        try:
            self.cursor.execute(push_task_query, (_query, 'WAITING'))
            self.conn.commit()
            self.close()
        except sqlite3.OperationalError as e:
            lgr.error("Error pushing task to task_queue: {}".format(e))

    def get_task(self, _id) -> list:
        self.connect()

        get_task_query = '''
            SELECT COUNT(*) FROM task_queue WHERE id=?
        '''
        try:
            r = self.cursor.execute(get_task_query,(_id))
            self.conn.commit()
            self.close()
            return r
        except sqlite3.OperationalError as e:
            lgr.error("Error getting task from task_queue: {}".format(e))
            return []
        

    def del_task(self, _id) -> None:
        self.connect()

        del_task_query = '''
            DELETE FROM task_queue WHERE id=?
        '''

        try:
            self.cursor.execute(del_task_query, (_id))
            self.conn.commit()
            self.close()
        except sqlite3.OperationalError as e:
            lgr.error("Error deleting task from task_queue: {}".format(e))

    def next_task(self) -> dict:
        self.connect()

        next_task_query = '''
            SELECT * FROM task_queue WHERE status=?
        '''

        try:
            r = self.cursor.execute(next_task_query, ("WAITING"))
            self.close()
            return r[0]
        except sqlite3.OperationalError as e:
            lgr.error("Error getting next task from task_queue: {}".format(e))
            return {}

    def all_tasks(self) -> list:
        self.connect()

        get_all_tasks = '''
            SELECT * FROM task_queue
        '''
        try:
            r = self.cursor.execute(get_all_tasks)
            self.close()
            return r
        except sqlite3.OperationalError as e:
            lgr.error("Error getting all tasks from task_queue: {}".format(e))
            return []


