'''DrOpt controller.

This is the DrOpt project control script.
It encapsulates the procedure for creating and running a DrOpt project
by standardizing the required model file and the config file.

Usage:
  Run the following command under the directory storing your DrOpt
  project (which typically includes 'model.py' and 'config.json'):

    $ droptctl -t [user token] -i [server IP] -c [configuration file]

  See the online help for details.


Todo:
  - Enable different commands for droptctl.
'''


import sys
import importlib.util
import json
from argparse import ArgumentParser, SUPPRESS
from time import sleep

from dropt.client.interface import Connection
from dropt.cmd.execute import execute_cmd, update_progress_file, project_log


def header_footer_loop(func):
    '''Decorator tha includes header, footer and trial loop for projects.'''
    def wrapper(project, model, params, pid, n_trial, progress):
        # header
        print(f'\n=================== Trial Start ====================')
        print(f'\t\tProject ID: {pid}')
        print(f'----------------------------------------------------')

        # trial loop
        for i in range(progress, n_trial):
            print(f'\n[trial {i+1}/{n_trial}]')
            func(project, model, params)
        
        # save project log
        # project_log['status'] = 'done'
        update_progress_file(project_log['project_id'], 'done')
        
        # footer
        print('\n=================== Trial End ======================\n')
    return wrapper


@header_footer_loop
def param_search(project, model, params):
    '''Parameter search and evaluation.'''
    # wait for back-end processing
    sleep(2)

    # request hyper-parameters from DrOpt
    sugt = project.suggestions().create()
    sugt_id = sugt.suggest_id
    sugt_value = sugt.assignments

    # evaluate the model with the suggested parameter configuration
    params.update(sugt_value)
    print(f"Suggestion = {sugt_value}")
    try:
        metric = model.run(params)
    except RuntimeError as exc:
        print(exc)
        print('Please add RuntimeError handler in your model code.')
        sys.exit(1)
    print(f"Evaluation: {metric}")

    # report result to DrOpt
    project.validations().create(suggest_id=sugt_id, value=metric)

    # update project_log
    update_progress_file(project_log['project_id'])

def start():
    '''Main procedure for creating and running a project.'''
    # parse input arguments
    parser = ArgumentParser(prog='droptctl', description='Create DrOpt projects.')
    parser.add_argument('command', metavar='CMD', type=str, nargs='?',
                         help='the action that will be executed by droptctl', default='create')
    parser.add_argument('-t', '--token', help='user token', required=True)
    parser.add_argument('-s', '--server', default='dropt.neuralscope.org',
                        help='server address (default: dropt.neuralscope.org/)')
    parser.add_argument('-c', '--config', default='config.json',
                        help='config file (default: ./config.json)')
    parser.add_argument('-p', '--port', default='',
                        help=SUPPRESS)
    args, _ = parser.parse_known_args()

    # read config file
    with open(args.config, 'r') as file:
        conf = json.load(file)

    # load model
    model_name = conf['config']['model']
    spec = importlib.util.spec_from_file_location(model_name, f'{model_name}.py')
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)

    # establish connection to the given DrOpt server with the given user token
    conn = Connection(client_token=args.token, server_ip=args.server, server_port=args.port)

    # execute the given command
    pid, n_trial, progress, project = execute_cmd(args.command, conn, conf)

    # perform parameter search and evaluation
    param_search(project, model, conf['params'], pid, n_trial, progress)


if __name__ == '__main__':
    start()
