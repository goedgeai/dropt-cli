'''Logging utilities for DrOpt packages.'''


import logging
import functools
from pathlib import Path
from datetime import date


class Logger:
    '''Wrapping class for logger.'''

    # logging format
    dfmt = '%Y%m%d'
    dtfmt = '%Y-%m-%d %H:%M:%S'
    chfmt = '[%(asctime)s] %(name)s [%(levelname)s] %(message)s'
    chformatter = logging.Formatter(chfmt, dtfmt)
    fhfmt = '%(asctime)s|%(name)s|%(levelname)s|%(message)s'
    fhformatter = logging.Formatter(fhfmt, dtfmt)

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
        ch.setFormatter(cls.chformatter)
        return ch

    @classmethod
    def _create_file_handler(cls, level, **kwargs):
        '''A class method that creates a logging file handler.

        "kwargs" consists of arguments for logging.FileHandler,
        which should contain at least "filename."
        '''
        kwargs['filename'] = Path(kwargs['filename'])
        kwargs['filename'].parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(**kwargs)
        fh.setLevel(level)
        fh.setFormatter(cls.fhformatter)
        return fh


class DrOptLogger(Logger):
    '''Logger class for DrOpt'''

    name = 'dropt'

    def __init__(self, suffix=None, ch_level=logging.WARNING, fh_level=logging.INFO, log_dir='/tmp/dropt/'):
        # logger name
        if suffix:
            name = f'{self.name}.{suffix}'
        else:
            name = self.name

        # console handler
        ch = self._create_console_handler(ch_level)

        # file handler
        log_dir = Path(log_dir)
        date_str = date.today().strftime(self.dfmt)
        filename = log_dir.joinpath(f'{name}_{date_str}.log')
        fh = self._create_file_handler(fh_level, filename=filename)

        # logger
        logger = self._create_logger(name)

        # initialize the logging object
        super().__init__(logger, [ch, fh])


class DrOptServiceLogger(DrOptLogger):
    '''Logger class for DrOpt service.'''

    name = 'dropt.srv'


class DrOptClientLogger(DrOptLogger):
    '''Logger class for DrOpt client.'''

    name = 'dropt.client'


class DrOptUserLogger(DrOptLogger):
    '''Logger class for DrOpt project.'''

    name = 'dropt.user'

    def __init__(self, suffix=None, ch_level=logging.WARNING, fh_level=logging.INFO, log_dir='log/'):
        super().__init__(suffix, ch_level, fh_level, log_dir)


class FuncLoggingWrapper:
    '''Logging wrapping class for function.'''
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
