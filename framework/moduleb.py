
import crud
from logger import get_logger

class mobase(crud.database):

    def __init__(self, name, desc, ver) -> None:
        self.name = name | "Module"
        self.description = desc | "This is a sample Description"
        self.version = ver | "0.0.1"

    def logger(self, name):
        return get_logger(name)

    