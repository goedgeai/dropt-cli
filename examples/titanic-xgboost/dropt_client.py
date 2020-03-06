"""Example DrOpt client script.

This script demonstrates how one can wrap a python ML model
training/testing script with a DrOpt client script in order to submit
an experiment to a DrOpt server.

Example:
    Before running
    To run the script, simply execute the following command in shell:

        $ python dropt_client -t [user token] -i [server IP] -c [configuration file]
"""

import time
import dropt.client as dropt_cli
from argparse import ArgumentParser
from subprocess import check_output


# parse input arguments
parser = ArgumentParser()
parser.add_argument("-t", "--user-token", help="user token", required=True)
parser.add_argument("-i", "--server-ip", help="server IP", required=True, default="52.175.54.152")
parser.add_argument("-c", "--config", help="configuration file", required=True, default="config.json")
args, _ = parser.parse_known_args()

# establish connection to a DrOpt server using the given user token
conn = dropt_cli.Connection(client_token=args.user_token, server_ip=args.server_ip)

# create a DrOpt project
project = conn.projects().create(
   config = dropt_cli.load_config_file(args.config)
)

# Get project ID and trial ID that are returned from DrOpt server
project_id = project.project_id
trial_number = project.trial

print( "\n=================== Trial Start ====================")
print(f"        Project ID: {project_id}, Trial number: {trial_number}")
print( "----------------------------------------------------")

# Run the optimization loop
for i in range(trial_number):
    # Delay wait for backend processing
    time.sleep(1)

    # Retrieve hyper-paramaters from DrOpt
    sugt = conn.projects(project_id).suggestions().create()
    sugt_id = sugt.suggest_id
    params = suggestion.assignments

    metric = train(params)
    print(f"\n[trial {i+1}] Evaluation: {metric}")
    print(f"suggestion = {sugts}")

    # report to DrOpt
    conn.projects(project_id).validations().create(
        suggest_id = sugt_id,
        value = float(metric)
    )

print("\n=================== Trial End ======================\n")


def evaluate(params):
    params = {p: str(params[p]) for p in params}
    out = check_output(["python3", "main.py",
        "-d", params["max_depth"],
        "-g", params["gamma"],
        "-s", params["subsample"],
        "-c", params["colsample"],
        "-a", params["alpha"],
        "-l", params["learn_rate"]
    ])
    
    return str(out, encoding = "utf-8")[0:5]


def header_footer_loop(*args, **kwargs):
    print( "\n=================== Trial Start ====================")
    print(f"        Project ID: {project_id}, Trial number: {trial_number}")
    print( "----------------------------------------------------")

    print("\n=================== Trial End ======================\n")


def param_search():
    # wait for back-end processing
    time.sleep(1)

    # request hyper-parameters from DrOpt
    sugt = conn.projects(project_id).suggestions().create()
    sugt_id = sugt.suggest_id
    params = suggestion.assignments

    metric = train(params)
    print(f"\n[trial {i+1}] Evaluation: {metric}")
    print(f"suggestion = {sugts}")

    # report to DrOpt
    conn.projects(project_id).validations().create(
        suggest_id = sugt_id,
        value = float(metric)
    )
