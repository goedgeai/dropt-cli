'''
Reference
---
https://en.wikipedia.org/wiki/Test_functions_for_optimization
'''


import argparse
import logging


# setup logs
logger = logging.getLogger("test_function_for_optimization")


def get_params():
    '''get parameters'''
    parser = argparse.ArgumentParser(description='Rosenbrock function')
    parser.add_argument('-x', '--input_vector', nargs='+')

    args, _ = parser.parse_known_args()
    return [float(xi) for xi in args.input_vector]


def main(x):
    '''Evaluate the test function'''
    value = 0
    for i in range(len(x)-1):
        value = value + 100*(x[i+1]-x[i]**2)**2+(1-x[i])**2
    return value
    logger.debug(f"value = {value}")


if __name__ == '__main__':
    x = get_params()
    logger.debug(x)
    value = main(x)
    print(value)
