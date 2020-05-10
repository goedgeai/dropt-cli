"""Logging utilities for DrOpt packages.

Here I follow the suggestion on
https://bbengfort.github.io/snippets/2016/01/11/logging-mixin.html
"""


import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import date


# constants


class Logger:
    '''Wrapping class for logger.'''

    # class variables regarding logging format
    fmt = '[%(asctime)s] %(name)s@%(module)s [%(levelname)s] %(message)s'
    dtfmt = '%Y-%m-%d %H:%M:%S'
    dfmt = '%Y%m%d'
    formatter = logging.Formatter(fmt, dtfmt)

    def __init__(self, logger):
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

    def __create_logger__(name, level, handlers):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        for hand in handlers:
            logger.addHandler(hand)
        return logger

    def __create_console_handler__(level):
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(FORMATTER)
        pass

    def __create_file_handler__(log_path, level):
        pass


class DroptServiceLogger(DroptLogger):
    def __init__(self, ch_level, fh_level, log_dir=Path('/tmp/dropt/'))
        # logger name
        name = 'dropt.srv'

        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(ch_level)
        ch.setFormatter(LOGFMT)

        # file handler
        log_dir = Path(log_dir)
        date_str = date.today().strftime(DFMT)
        log_path = log_dir.joinpath(f'{name}-{date_str}.log')
        fh = logging.FileHandler(logfilepath.joinpath(f'{name}-{date_str}.log'))
        fh.setLevel(fh_level)
        fh.setFormatter(LOGFMT)

        # logger
        logger = logging.getLogger(name)
        logger = setLevel(min(ch_level, fh_level))
        logger.addHandler(ch)
        logger.addHandler(fh)

        super().__init__(logger)


class DroptClientLogger(Logger):
    def __init__(self, ch_level, fh_level, log_dir=Path('/tmp/dropt/'))
        # logger name
        name = 'dropt.cli'

        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(ch_level)
        ch.setFormatter(LOGFMT)

        # file handler
        log_dir = Path(log_dir)
        date_str = date.today().strftime(DFMT)
        log_path = log_dir.joinpath(f'{name}-{date_str}.log')
        fh = logging.FileHandler(log_path)
        fh.setLevel(fh_level)
        fh.setFormatter(LOGFMT)

        # logger
        logger = logging.getLogger(name)
        logger = setLevel(min(ch_level, fh_level))
        logger.addHandler(ch)
        logger.addHandler(fh)

        super().__init__(logger)


class DroptProjectLogger(DroptLogger):
    def __init__(self, proj_name, ch_level, fh_level, log_dir=Path('/tmp/dropt/'))
        # logger name
        name = 'dropt.project'

        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(ch_level)
        ch.setFormatter(LOGFMT)

        # file handler
        log_dir = Path(log_dir)
        date_str = date.today().strftime(DFMT)
        fh = logging.FileHandler(logfilepath.joinpath(f'{name}-{date_str}.log'))
        fh.setLevel(fh_level)
        fh.setFormatter(LOGFMT)

        # logger
        logger = logging.getLogger(name)
        logger = setLevel(min(ch_level, fh_level))
        logger.addHandler(ch)
        logger.addHandler(fh)

        super().__init__(logger)
