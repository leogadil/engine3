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
import crud

class activememory():

    def __init__(self) -> None:
        super().__init__("./activememory/shortterm_memory.db")
        self.task = None

    def init_task(self):
        self.task = taskactivememory('./activememory/task_memory.db')


class taskactivememory(crud.database):

    def __init__(self, db_path: str) -> None:
        super().__init__(db_path)

    def create_task_memory(self) -> None:
        """
        create a database table for tasks queue
        """

        task_memory_query = '''
            CREATE TABLER IF NOT EXIST task_queue(
                id STRING PRIMARY KEY,
                query STRING,
                status STRING
            )
        '''

        self.execute(task_memory_query)

    def push_task(self, _query) -> None:
        self.connect()

        push_task_query = '''
            INSERT INTO task_queue(id, query, status) values(?,?,?)
        '''

        self.cursor.execute(push_task_query, (_query, 'WAITING'))
        self.conn.commit()
        self.close()

    def get_task(self, _id) -> list:
        self.connect()

        get_task_query = '''
            SELECT COUNT(*) FROM task_queue WHERE id=?
        '''

        r = self.cursor.execute(get_task_query,(_id))
        self.conn.commit()
        self.close()
        return r
        

    def del_task(self, _id) -> None:
        self.connect()

        del_task_query = '''
            DELETE FROM task_queue WHERE id=?
        '''

        self.cursor.execute(del_task_query, (_id))
        self.conn.commit()
        self.close()

    def next_task(self) -> dict:
        self.connect()

        next_task_query = '''
            SELECT * FROM task_queue WHERE status=?
        '''

        r = self.cursor.execute(next_task_query, ("WAITING"))
        self.close()
        return r[0]

    def all_tasks(self) -> list:
        self.connect()

        get_all_tasks = '''
            SELECT * FROM task_queue
        '''

        r = self.cursor.execute(get_all_tasks)
        self.close()
        return r

