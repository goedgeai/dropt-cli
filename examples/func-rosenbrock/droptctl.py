"""DrOpt controller

This is the controller of DrOpt experiments.

Example:
    To run the script, simply execute the following command in shell:

        $ droptctl -t [user token] -i [server IP] -c [configuration file]
"""


import dropt.client as dropt_cli
import json
import time
from argparse import ArgumentParser
from importlib import import_module
from rosenbrock import run, params


def header_footer_loop(func):
    '''Decorator for header, footer and loop.'''
    def inner(p, model, pid, n_trial):
        print( "\n=================== Trial Start ====================")
        print(f"        Project ID: {pid}, Number of trials: {n_trial}")
        print( "----------------------------------------------------")
        for i in range(n_trial):
            print(f"\n[trial {i+1}]")
            func(p, model)
        print("\n=================== Trial End ======================\n")
    return inner
    

@header_footer_loop
def param_search(p, model):
    '''Parameter search.'''
    # wait for back-end processing
    time.sleep(2)

    # request hyper-parameters from DrOpt
    sugt = p.suggestions().create()
    sugt_id = sugt.suggest_id
    sugt_value = sugt.assignments

    # apply the suggested parameters and evalute the corresponding model
    model.params.update(sugt_value)
    metric = model.run(params)
    print(f"Suggestion = {sugt_value}")
    print(f"Evaluation: {metric}")

    # report result to DrOpt
    p.validations().create(suggest_id=sugt_id, value=metric)


def start():
    # parse input arguments
    parser = ArgumentParser()
    parser.add_argument("-t", "--user-token", help="user token", required=True)
    parser.add_argument("-s", "--server-ip", help="server IP address", default="140.113.213.86")
    parser.add_argument("-c", "--config", help="configuration file", default="config.json")
    args, _ = parser.parse_known_args()

    # read config file
    with open(args.config, 'r') as f:
        conf = json.load(f)

    # load model
    model = import_module(conf['config']['model'])

    # establish connection to a DrOpt server with the given user token
    conn = dropt_cli.Connection(client_token=args.user_token, server_ip=args.server_ip)

    # create a DrOpt project
    project = conn.projects().create(config = json.dumps(conf))

    pid = project.project_id
    n_trial = project.trial
    p = conn.projects(pid)

    # perform parameter search
    param_search(p, model, pid, n_trial)


if __name__ == '__main__':
    start()
