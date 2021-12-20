# stolen from https://gist.github.com/batzner/82d2982e363673a9852254e49d41405d
# thank you https://gist.github.com/batzner

"""Helper module for logging.
Example Usage:
from log import get_logger, get_out_dir_of_logger
LOG = get_logger(__name__)
LOG.info('Logging to %s' % get_out_dir_of_logger(LOG))
"""

import os
import logging
import socket
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional
from colorama import Fore, init

init(
    autoreset=True,
)

# THINGS YOU MIGHT WANT TO CUSTOMIZE

CONSOLE_LEVEL = logging.DEBUG
CONSOLE_FORMAT = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'

# FILE_LEVELS should be the tuples of log levels with the corresponding log
# file name
FILE_LEVELS = [(logging.DEBUG, 'debug.log'), (logging.INFO, 'info.log')]
FILE_FORMAT = '%(asctime)s - %(host)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S %z'


def create_log_dir() -> Optional[str]:
    """Creates a new log directory for the current run.
    You can also modify this to return None in some cases. Then nothing will
    get logged to file s, only to console.
    """
    time_str = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S-%f')
    log_dir = './logs/%s/' % time_str
    # log_dir = os.path.expanduser(log_dir)
    log_dir = os.path.join(os.getcwd(), log_dir)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


# END OF THINGS YOU MIGHT WANT TO CUSTOMIZE

class CustomFormatter(logging.Formatter):

    err_fmt = f'{Fore.LIGHTRED_EX}%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    dbg_fmt = f'{Fore.LIGHTCYAN_EX}%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    wrng_fmt = f'{Fore.YELLOW}%(asctime)s | %(name)s | %(levelname)s | %(message)s'

    def __init__(self, fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s', datefmt=DATE_FORMAT):
        super().__init__(fmt=fmt, datefmt=datefmt, style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = CustomFormatter.dbg_fmt

        elif record.levelno == logging.WARNING:
            self._style._fmt = CustomFormatter.wrng_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = CustomFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


class HostLogger(logging.Logger):
    """Adds the host name to each log statement."""

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False):
        if extra is None:
            extra = {}
        extra['host'] = socket.gethostname()
        super()._log(level, msg, args, exc_info, extra, stack_info)


# Use a single log dir by default for get_log_dir() calls
_log_dir = None


def get_log_dir() -> str:
    """Returns the log directory for the current run."""
    global _log_dir
    if _log_dir:
        # Reuse the existing log directory
        return _log_dir
    else:
        # Create a new log directory
        _log_dir = create_log_dir()
        return _log_dir


def get_logger(name: str, log_dir: str = None) -> logging.Logger:
    """Returns the central logger."""
    log_dir = log_dir if log_dir else get_log_dir()
    if log_dir is None:
        print('WARNING: log %s will not be logged to any file, only to '
              'console.' % name)

    # Create a custom logger
    logger = logging.getLogger(name)

    # Create the console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # console_format = logging.Formatter(
    #     fmt=CONSOLE_FORMAT,
    #     datefmt=DATE_FORMAT
    # )
    # console_handler.setFormatter(console_format)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # Create the file logging
    if log_dir and FILE_LEVELS:
        for log_level, file_name in FILE_LEVELS:
            add_file_handler(logger, log_dir, file_name, log_level)
    return logger


def get_out_dir_of_logger(logger: logging.Logger):
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return os.path.dirname(handler.baseFilename)
    return None


def add_file_handler(logger: logging.Logger, log_dir: str, file_name: str,
                     log_level):
    os.makedirs(log_dir, exist_ok=True)

    file_path = os.path.join(log_dir, file_name)
    file_handler = RotatingFileHandler(file_path, maxBytes=2000000,
                                       backupCount=5)
    file_handler.setLevel(log_level)
    file_format = logging.Formatter(
        fmt=FILE_FORMAT,
        datefmt=DATE_FORMAT)
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)


def _init_module():
    logging.setLoggerClass(HostLogger)

    # Change the root level to lowest
    logging.getLogger().setLevel(logging.DEBUG)


_init_module()