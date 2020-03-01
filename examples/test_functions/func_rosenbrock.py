'''
Reference
---
https://en.wikipedia.org/wiki/Test_functions_for_optimization
'''

import logging
import argparse


# setup logs
logger = logging.getLogger("test_function_for_optimization")


def get_x():
    '''get parameters'''
    parser = argparse.ArgumentParser(description='Rosenbrock function')
    parser.add_argument('-x', '--input_vector', nargs='+', dest='x')

    args, _ = parser.parse_known_args()
    return [float(xi) for xi in args.x]


def main(x):
    '''Evaluate the test function'''
    y = 0
    for i in range(len(x)-1):
        y = y + 100*(x[i+1]-x[i]**2)**2+(1-x[i])**2
    return y
    logger.debug(f"y: {y}")


if __name__ == '__main__':
    x = get_x()
    logger.debug(x)
    y = main(x)
    print(y)
