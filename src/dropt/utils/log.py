"""Logging utilities for DrOpt packages.

Here I follow the suggestion on
https://bbengfort.github.io/snippets/2016/01/11/logging-mixin.html
"""


import logging
import functools
from pathlib import Path
from datetime import date


class Logger:
    '''Wrapping class for logger.'''

    # logging format
    fmt = '[%(asctime)s] %(name)s [%(levelname)s] %(message)s'
    dtfmt = '%Y-%m-%d %H:%M:%S'
    dfmt = '%Y%m%d'
    formatter = logging.Formatter(fmt, dtfmt)

    def __init__(self, logger, handlers):
        level = min([h.level for h in handlers])
        logger.setLevel(level)
        for h in handlers:
            logger.addHandler(h)
        self._logger = logger

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    @classmethod
    def _create_logger(cls, name):
        logger = logging.getLogger(name)
        return logger

    @classmethod
    def _create_console_handler(cls, level):
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(cls.formatter)
        return ch

    @classmethod
    def _create_file_handler(cls, log_path, level):
        log_path = Path(log_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_path)
        fh.setLevel(level)
        fh.setFormatter(cls.formatter)
        return fh


class DroptServiceLogger(Logger):
    def __init__(self, ch_level=logging.WARNING, fh_level=logging.INFO, log_dir='/tmp/dropt/'):
        # logger name
        name = 'dropt.srv'

        # console handler
        ch = super()._create_console_handler(ch_level)

        # file handler
        log_dir = Path(log_dir)
        date_str = date.today().strftime(super().dfmt)
        log_path = log_dir.joinpath(f'{name}-{date_str}.log')
        fh = super()._create_file_handler(log_path, fh_level)

        # logger
        logger = super()._create_logger(name)

        # initialize the logging object
        super().__init__(self, logger, [ch, fh])


class DroptClientLogger(Logger):
    def __init__(self, ch_level=logging.WARNING, fh_level=logging.INFO, log_dir='/tmp/dropt/'):
        # logger name
        name = 'dropt.cli'

        # console handler
        ch = super()._create_console_handler(ch_level)

        # file handler
        log_dir = Path(log_dir)
        date_str = date.today().strftime(super().dfmt)
        log_path = log_dir.joinpath(f'{name}-{date_str}.log')
        fh = super()._create_file_handler(log_path, fh_level)

        # logger
        logger = super()._create_logger(name)

        # initialize the logging object
        super().__init__(self, logger, [ch, fh])


class DroptUserLogger(Logger):
    def __init__(self, name, ch_level=logging.WARNING, fh_level=logging.INFO, log_dir='log/'):
        # logger name
        name = f'dropt.project.{name}'

        # console handler
        ch = super()._create_console_handler(ch_level)

        # file handler
        log_dir = Path(log_dir)
        date_str = date.today().strftime(super().dfmt)
        log_path = log_dir.joinpath(f'{name}-{date_str}.log')
        fh = super()._create_file_handler(log_path, fh_level)

        # logger
        logger = super()._create_logger(name)

        # initialize the logging object
        super().__init__(logger, [ch, fh])


class FuncLoggingWrapper:
    def __init__(self, logger):
        self._logger = logger

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self._logger.debug(f'Entering function "{func.__name__}".')
            r = func(*args, **kwargs)
            self._logger.debug(f'Exiting function "{func.__name__}".')
            return r
        return wrapper
