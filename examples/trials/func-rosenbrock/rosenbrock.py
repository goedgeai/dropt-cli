'''
Reference
---
https://en.wikipedia.org/wiki/Test_functions_for_optimization
'''


from dropt.util.log import UserLogger
from pathlib import Path
from argparse import ArgumentParser
import logging


# logger
logger_name = Path(__FILE__).stem
logger = UserLogger(logger_name)
logger.add_console_handler(logging.INFO)
logger.add_file_handler(logging.INFO, filename=f'{logger_name}.log')


def run(params):
    '''Evaluate the test function'''
    x = params['x']
    y = params['y']
    z = params['z']
    value = 0
    value = value + 100*(y-x**2)**2+(1-x)**2
    value = value + 100*(z-y**2)**2+(1-y)**2
    logger.debug(f"value = {value}")
    return value


def param_loader():
    '''Get parameters'''
    parser = ArgumentParser(description='Rosenbrock function')
    parser.add_argument('x', type=float)
    parser.add_argument('y', type=float)
    parser.add_argument('z', type=float)

    args, _ = parser.parse_known_args()
    return vars(args)


if __name__ == '__main__':
    params = param_loader()
    logger.debug(f'parameters = {params}')
    print(run(params))
