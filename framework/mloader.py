
import os
from pathlib import Path

class loader:

    def __init__(self, path: str):
        self.path = os.path.join(Path(__file__).parent, path)
        self.files = []
        self.load()

    def load(self) -> None:
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".py"):
                    self.files.append(os.path.join(root, file))

    def get_files(self) -> list:
        return self.files

    def get_path(self) -> str:
        return self.path

if __name__ == '__main__':
    l = loader('modules')
    print(l.get_files())