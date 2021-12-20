
from moduleb import mobase

class weather(mobase):

    def __init__(self) -> None:
        super().__init__(
                "Weather", 
                "Manages Weather", 
                "0.0.1"
            )
        self.lgr = self.logger(__name__)
        self.lgr.info('This is working')
        