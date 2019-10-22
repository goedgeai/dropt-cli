import dropt
import time
import argparse as arg
from subprocess import check_output

parser = arg.ArgumentParser()
parser.add_argument("-token", "--user-api-token", help="user api token", dest="token", default="")
parser.add_argument("-proj-name", "--project-name", help="project name", dest="name", default="")
parser.add_argument("-ip", "--server-ip", help="server ip", dest="ip", default="")
parser.add_argument("-trial", "--trial-num", help="trail num", dest="trial", default=10)
args = parser.parse_args()

# Define API token for authorization
conn = dropt.Connection(client_token=args.token, server_ip=args.ip)

# Create DrOpt project
project = conn.projects().create(
   # Define project name
   name=args.name,
   # Define which parameters you would like to tune
   # type: int - means integer parameter
   # type: float - means float parameter
   # type: choice - means categorical parameter
   parameters=[
     {'name': 'max_depth', 'type': 'int', 'min': 1,  'max': 5},
     {'name': 'gamma', 'type': 'float', 'min': 0.1,  'max': 1.0},
     {'name': 'subsample', 'type': 'float', 'min': 0.1, 'max': 1.0},
     {'name': 'colsample', 'type': 'float', 'min': 0.1, 'max': 1.0},
     {'name': 'alpha', 'type': 'float', 'min': 0.1, 'max': 1.0},
     {'name': 'learn_rate', 'type': 'float', 'min': 0.1, 'max': 1.0}
     # {'name': 'tcrang', 'type': 'choice', 'value': 'aaa,bbb,ccc,ddd,eee'},
   ],
   # tuner='auto', # or 'TPE,'
   # Define the validation times for your project (optimization loops)
   trial=args.trial,
)

# Get project id that returned from DrOpt
project_id = project.project_id
project_trial = project.trial
print ("\n=================== Trial Start ====================")
# print ("----------------------------------------------------")
print ("        Project ID: %s, Project Trial: %s" % (project_id, project_trial))
print ("----------------------------------------------------")

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
    return str(out, encoding = "utf-8")[0:5]


# Run the optimization loop
for i in range(project_trial):
   # Retrieve hyperparamaters from DrOpt
   suggestion = conn.projects(project_id).suggestions().create()
   sugt_id = suggestion.suggest_id
   sugts = suggestion.assignments

   metric = train(params=sugts)
   print('\n[trial %d] Evaluation: %s' % (i+1, metric))
   print("suggestion="+str(sugts))

   # report to DrOpt
   conn.projects(project_id).validations().create(
     suggest_id = sugt_id,
     value = float(metric),
   )

   # Delay wait for backend processing
   time.sleep(1)
