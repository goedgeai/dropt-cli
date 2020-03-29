'''
Reference
---
https://en.wikipedia.org/wiki/Test_functions_for_optimization
'''


import logging
from argparse import ArgumentParser
from math import sin, sqrt


# setup logs
logger = logging.getLogger("test_function_for_optimization")


def run(params):
    '''Evaluate the test function'''
    x = params['x']
    y = params['y']
    value = -(y+47)*sin(sqrt(abs(x/2+(y+47))))-x*sin(sqrt(abs(x-(y+47))))
    logger.debug(f"value = {value}")
    return value


def param_loader():
    '''Get parameters'''
    parser = ArgumentParser(description='Eggholder function')
    parser.add_argument('-x', type=float, required=True)
    parser.add_argument('-y', type=float, required=True)

    args, _ = parser.parse_known_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    params = param_loader()
    logger.debug(f'parametrs = {params}')
    print(run(params))
