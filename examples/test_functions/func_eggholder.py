'''
Reference
---
https://en.wikipedia.org/wiki/Test_functions_for_optimization
'''


import argparse
import logging
from math import sin, sqrt


# setup logs
logger = logging.getLogger("test_function_for_optimization")


def get_params():
    '''get parameters'''
    parser = argparse.ArgumentParser(description='Eggholder function')
    parser.add_argument('-x', '--input_x', type=float)
    parser.add_argument('-y', '--input_y', type=float)

    args, _ = parser.parse_known_args()
    return args.input_x, args.input_y


def main(x, y):
    '''Evaluate the test function'''
    value = -(y+47)*sin(sqrt(abs(x/2+(y+47))))-x*sin(sqrt(abs(x-(y+47))))
    logger.debug(f"value = {value}")
    return value


if __name__ == '__main__':
    x, y = get_params()
    logger.debug(x, y)
    value = main(x, y)
    print(value)
