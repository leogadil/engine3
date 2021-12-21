
import abc
import threading

import crud
from logger import get_logger


class mobase(crud.database):

    def __init__(self, name, desc, ver) -> None:
        self.name = name
        self.description = desc
        self.version = ver

    def logger(self, name):
        return get_logger(name)

    @abc.abstractmethod
    def run(self):
        pass
    
    @staticmethod
    def run_in_thread(fn):
        def run(*k, **kw):
            t = threading.Thread(target=fn, args=k, kwargs=kw)
            t.daemon = True
            t.start()
            return t # <-- this is new!
        return run

    