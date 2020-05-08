"""Logging utilities for DrOpt packages.

Here I follow the suggestion on
https://bbengfort.github.io/snippets/2016/01/11/logging-mixin.html



"""


import logging
import logging.config


config = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(name)s/%(levelname)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },

    'loggers': {
        'logger1': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        }
    }
}

logging.config.dictConfigClass(config).configure()


#default_fmt = logging.Formatter('[%(asctime)s] %(name)s/%(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
