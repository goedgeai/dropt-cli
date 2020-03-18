"""DrOpt client

This script controls DrOpt experiments.

Example:
    To run the script, simply execute the following command in shell:

        $ droptctl -t [user token] -i [server IP] -c [configuration file]
"""


import time
import dropt.client as dropt_cli
from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path


def header_footer_loop(func):
    '''Header, footer and loop of the experiment.'''
    def inner(pid, n_trial):
        print( "\n=================== Trial Start ====================")
        print(f"        Project ID: {pid}, Number of trials: {n_trial}")
        print( "----------------------------------------------------")
        for i in range(n_trial):
            print(f"\n[trial {i+1}]")
            func(pid, n_trial)
        print("\n=================== Trial End ======================\n")
    return inner
    

@header_footer_loop
def param_search(pid, n_trial):
    '''Parameter search.'''
    # wait for back-end processing
    time.sleep(2)

    # request hyper-parameters from DrOpt
    sugt = conn.projects(pid).suggestions().create()
    sugt_id = sugt.suggest_id
    sugt_value = sugt.assignments

    # apply the suggested parameters and evalute the corresponding model
    params.update(sugt_value)
    metric = run(params)
    print(f"Suggestion = {sugt_value}")
    print(f"Evaluation: {metric}")

    # report result to DrOpt
    conn.projects(pid).validations().create(
        suggest_id = sugt_id,
        value = metric
    )


def start():
    # parse input arguments
    parser = ArgumentParser()
    parser.add_argument("-t", "--user-token", help="user token", required=True)
    parser.add_argument("-i", "--server-ip", help="server IP", default="52.175.54.152")
    parser.add_argument("-c", "--config", help="configuration file", default="config.json")
    args, _ = parser.parse_known_args()

    # establish connection to a DrOpt server using the given user token
    conn = dropt_cli.Connection(client_token=args.user_token, server_ip=args.server_ip)

    # create a DrOpt project
    project = conn.projects().create(
       config = dropt_cli.load_config_file(args.config)
    )

    # perform parameter search
    param_search(pid=project.project_id, n_trial=project.trial)


if __name__ == '__main__':
    start()
