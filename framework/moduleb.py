
import abc
import atexit
import json
import os
import threading

import crud
from helper import timehelper
from idgen import genid
from location import location
from logger import get_logger

lgr = get_logger(__name__)

class mobase(crud.database, timehelper):

    def __init__(self, name, desc, ver) -> None:
        self.name = name.lower()
        self.description = desc
        self.version = ver
        self.http_host = None
        folder = 'framework/modules/{}'.format(self.name)
        if not os.path.exists(folder):
            lgr.warning('Creating folder: {}'.format(folder))
            os.makedirs(folder)

        self.config = json.load(open('framework/config.json'))

        self.loc = location()

        super().__init__('modules/{}/database.db'.format(self.name))

    def logger(self, name):
        return get_logger(name)

    @abc.abstractmethod
    def run(self):
        pass

    def create_id(self):
        return "{}_{}".format(self.name, genid())

    @staticmethod
    def search_location(query: str) -> dict:
        try:
            return location.get_location_from_query(query)
        except Exception as e:
            return {'error': str(e)}

    def ttime(self):
        return timehelper
    
    @staticmethod
    def run_in_thread(fn):
        def run(*k, **kw):
            t = threading.Thread(target=fn, args=k, kwargs=kw)
            t.daemon = True
            t.start()
            return t # <-- this is new!
        return run

    