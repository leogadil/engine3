import os

from logger import get_logger

lgr = get_logger(__name__)

class retentionmemory:

    def __init__(self) -> None:
        
        folder = 'framework/retention'
        if not os.path.exists(folder):
            lgr.warning(f'Creating folder: {folder}')
            os.makedirs(folder)