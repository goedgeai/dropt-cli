'''
Reference
---
https://en.wikipedia.org/wiki/Test_functions_for_optimization
'''


from math import sin, sqrt
from dropt.util.log import UserLogger
from pathlib import Path
from argparse import ArgumentParser
import logging


# logger
logger_name = Path(__file__).stem
logger = UserLogger(logger_name)
logger.add_console_handler(logging.INFO)
logger.add_file_handler(logging.INFO, filename=f'{logger_name}.log')


def run(params):
    '''Evaluate the test function'''
    logger.info(f'parameters = {params}')
    x = params['x']
    y = params['y']
    value = -(y+47)*sin(sqrt(abs(x/2+(y+47))))-x*sin(sqrt(abs(x-(y+47))))
    logger.info(f'function value = {value}')
    return value


def param_loader():
    '''Get parameters'''
    parser = ArgumentParser(description='Eggholder function')
    parser.add_argument('x', type=float)
    parser.add_argument('y', type=float)

    args, _ = parser.parse_known_args()
    return vars(args)


if __name__ == '__main__':
    logger.info('Evaluation of the eggholder function')
    params = param_loader()
    print(run(params))
