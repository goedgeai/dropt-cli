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


from dropt.client.interface import Connection
from dropt.cmd.execute import execute_cmd, update_progress_file, project_log
import importlib.util
import json
from time import sleep
from pkg_resources import get_distribution, DistributionNotFound
import argparse
import sys


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
    '''droptctl command parser.'''
    # info of droptctl
    parser = argparse.ArgumentParser(prog='droptctl',
                            description='Use command to control DrOpt project.',
                            epilog='Run "droptctl CMD -h" to learn more about a specific command.')
    parser.add_argument('-v', '--version', action='version', version=get_distribution('dropt-cli').version)

    # create subparesers for commands
    subparsers = parser.add_subparsers(title='commands', metavar='CMD')

    # command 'create' for creating a new project
    parser_create = subparsers.add_parser('create', help='create new project',
                                          description='Create new DrOpt project.')
    parser_create.add_argument('-t', '--token', help='user token', required=True)
    parser_create.add_argument('-s', '--server', metavar='ADDRESS',
                               default='dropt.neuralscope.org',
                               help='server address (default: %(default)s)')
    parser_create.add_argument('-c', '--config', metavar='FILENAME',
                               default='config.json',
                               help='config file (default: %(default)s)')
    parser_create.add_argument('-p', '--port',
                               default='',
                               help='port number')

    # command 'resume' for resuming a existing project
    parser_create = subparsers.add_parser('resume', help='resume an existing project',
                                          description='Create new DrOpt project.')

    # display help info if no argument is given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args, _ = parser.parse_known_args()
    kwargs = vars(args)
    args.func(**kwargs)

#   # read config file
#   with open(args.config, 'r') as file:
#       conf = json.load(file)

#   # load model
#   model_name = conf['config']['model']
#   spec = importlib.util.spec_from_file_location(model_name, f'{model_name}.py')
#   model = importlib.util.module_from_spec(spec)
#   spec.loader.exec_module(model)

#   # establish connection to the given DrOpt server with the given user token
#   conn = Connection(client_token=args.token, server_ip=args.server, server_port=args.port)

#   # execute the given command
#   pid, n_trial, progress, project = execute_cmd(args.command, conn, conf)

#   # perform parameter search and evaluation
#   param_search(project, model, conf['params'], pid, n_trial, progress)


if __name__ == '__main__':
    start()
