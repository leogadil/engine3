import imports
import personalassistant as pa
from logger import get_logger

lgr = get_logger(__name__)

class Samantha(pa.engine):

    def __init__(self) -> None:
        super().__init__(self)
        self.name = "Samantha"
        self.version = "0.0.1"
        self.description = "A female personal assistant"
        self.author = "Jann Leo Gadil"
        self.initialize()
        self.run()





if __name__ == '__main__':
    Samantha()





