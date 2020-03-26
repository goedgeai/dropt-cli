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


import importlib.util
import json
from dropt.client.interface import Connection
from time import sleep
from argparse import ArgumentParser


def header_footer_loop(func):
    '''Decorator tha includes header, footer and trial loop for projects.'''
    def inner(project, model, params, pid, n_trial):
        # header
        print( '\n=================== Trial Start ====================')
        print(f'\t\tProject ID: {pid}')
        print( '----------------------------------------------------')

        # trial loop
        for i in range(n_trial):
            print(f'\n[trial {i+1}/{n_trial}]')
            func(project, model, params)

        # footer
        print('\n=================== Trial End ======================\n')
    return inner
    

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
    metric = model.run(params)
    print(f"Suggestion = {sugt_value}")
    print(f"Evaluation: {metric}")

    # report result to DrOpt
    project.validations().create(suggest_id=sugt_id, value=metric)


def start():
    '''Main procedure for creating and running a project.'''
    # parse input arguments
    parser = ArgumentParser(prog='droptctl', description='Create DrOpt projects.')
    parser.add_argument('-t', '--token', help='user token', required=True)
    parser.add_argument('-s', '--server', help='server address', default='https://dropt.neuralscope.org/')
    parser.add_argument('-c', '--config', help='config file', default='config.json')
    args, _ = parser.parse_known_args()

    # read config file
    with open(args.config, 'r') as f:
        conf = json.load(f)

    # load model
    model_name = conf['config']['model']
    spec = importlib.util.spec_from_file_location(model_name, f'{model_name}.py')
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)

    # establish connection to the given DrOpt server with the given user token
    conn = Connection(client_token=args.token, server_ip=args.server)

    # create a DrOpt project
    project = conn.projects().create(config = json.dumps(conf))
    pid = project.project_id
    n_trial = project.trial
    project = conn.projects(pid)

    # perform parameter search and evaluation
    param_search(project, model, conf['params'], pid, n_trial)


if __name__ == '__main__':
    start()
