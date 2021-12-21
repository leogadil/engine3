
import os
from importlib.machinery import SourceFileLoader
from pathlib import Path

from logger import get_logger

lgr = get_logger(__name__)

class loader:

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
                    self.modules[name] = main()
                except AttributeError as e:
                    lgr.warning(f"Module {name} can't be found. {e}")

        return self

    def get_modules(self) -> None:
        self.files = []
        for root, dirs, files in os.walk(self.path):
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
