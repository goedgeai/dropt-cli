import dropt.client as dropt_cli
import time
import random
import argparse as arg
from subprocess import check_output

parser = arg.ArgumentParser()
parser.add_argument("-token", "--user-api-token", help="user api token", dest="token", required=True)
parser.add_argument("-ip", "--server-ip", help="server ip", dest="ip", required=True)
args = parser.parse_args()

# Define API token for authorization
conn = dropt_cli.Connection(client_token=args.token, server_ip=args.ip)

# Create DrOpt project
project = conn.projects().create(
   config = dropt_cli.load_config_file("config.json")
)

# Get project id that returned from DrOpt
project_id = project.project_id
project_trial = project.trial

print( "\n=================== Trial Start ====================")
print(f"        Project ID: {project_id}, Project Trial: {project_trial}")
print( "----------------------------------------------------")

# Delay wait for backend initialing
time.sleep(1)

def train(params):
    out = check_output(["python3", "train.py",
    "-d", params["max_depth"],
    "-g", params["gamma"],
    "-s", params["subsample"],
    "-c", params["colsample"],
    "-a", params["alpha"],
    "-l", params["learn_rate"]
    ])
    
    # Or return random number for sample (delete the check_ouput)
    # best_acc = random.uniform(0.5, 0.9)
    # return best_acc
    
    return str(out, encoding = "utf-8")[0:5]


# Run the optimization loop
for i in range(project_trial):
   # Retrieve hyperparamaters from DrOpt
   suggestion = conn.projects(project_id).suggestions().create()
   sugt_id = suggestion.suggest_id
   sugts = suggestion.assignments

   metric = train(params=sugts)
   print(f"\n[trial {i+1}] Evaluation: {metric}")
   print(f"suggestion={sugts}")

   # report to DrOpt
   conn.projects(project_id).validations().create(
     suggest_id = sugt_id,
     value = float(metric)
   )

   # Delay wait for backend processing
   time.sleep(1)
