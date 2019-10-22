# Dropt Client Readme
## 1. Create account and get token
### Go to [Dropt Website](https://140.113.24.232) and create an account by "New Customer"

![](https://i.imgur.com/OSLZaLE.png)

### Get the access token

After creating the account, click "My Account" -> "My tokens"

![](https://i.imgur.com/n0P5kXA.png)

The string on the "My tokens" page is your dropt client token.
(The USER_TOKEN in the following sample code)

![](https://i.imgur.com/QQvqHlc.png)

## 2. Run the Experiment
1. put the [Dropt package](http://dataarch.myDS.me/drive/d/f/516675319327891457) into your working directory
```
.
├── dropt
└── train.py
```
2. Insert Dropt API code in the original training program
```python
import dropt

# Define API token for authorization
conn = dropt.Connection(client_token=[USER_TOKEN])

# Create DrOpt project
project = conn.projects().create(
   # Define project name
   name=[MY_PROJECT],
   # Define which parameters you would like to tune
   # type: int - means integer parameter
   # type: float - means float parameter
   # type: choice - means categorical parameter
   parameters=[
     {'name': 'filter1', 'type': 'int', 'min': 16,  'max': 96},
     {'name': 'filter2', 'type': 'int', 'min': 16,  'max': 96},
     {'name': 'ksize', 'type': 'int', 'min': 3,  'max': 10},
     {'name': 'learn_rate', 'type': 'float', 'min': 0.00001, 'max': 0.01},
     {'name': 'hidint', 'type': 'choice', 'value': '60,100,125,150'}
     # {'name': 'hidfloat', 'type': 'choice', 'value': '1.2222,5.6666,3.4444,7.8888'},
     # {'name': 'tcrang', 'type': 'choice', 'value': 'aaa,bbb,ccc,ddd,eee'},
   ],
   
   # Define the validation times for your project (optimization loops)
   trial=25,
   
   # Tuner setting (not available now)
   # tuner=["auto", "TPE", ...]
)

# Get project id that returned from DrOpt
project_id = project.project_id
project_trial = project.trial

# Delay wait for backend initialing
time.sleep(1)

# Run the training
for i in range(project_trial):
   # Retrieve hyperparamaters from DrOpt
   suggestion = conn.projects(project_id).suggestions().create()
   sugts = suggestion.assignments
   
   """
   The return object "suggestion.assignments" is a dict 
   (please note that the values are strings)
   
   sugts = {
     'filter1': '64',
     'filter2': '32', 
     'ksize': '5'},
     'learn_rate': '0.001'},
     'hidint': '100'
   }
   """
   
   # The user's training fuction
   metric = train(filter1=['filter1'], filter2=['filter2'], ... )
   
   # report result to DrOpt
   conn.projects(project_id).validations().create(
     suggest_id = sugt_id,
     value = float(metric),
   )
```
3. Start training, and user can see the result on [dropt website](https://140.113.24.232)


## 3. Client Code Sample

### Training code and dropt client, please download from:
https://git.dataarch.myds.me/cysun/dropt_client_sample

```
.
├── dropt              // dropt package
├── dropt_client.py    // training program with dropt
├── titanic            // training data folder
└── train.py           // original training code (without dropt)
```


### Start Training

```
python3 dropt_client.py -token [USER_TOKEN] -proj-name [PROJ_NAME] -trial [TRAIL_NUM]
```
#### Please remember to fill the user token!
#### To execute the train.py in this package, you may need to install xgboost (pip install xgboost)


## 4. Result Analysis

When the training is done, the results and the analysis will be shown on the project list.

![](https://i.imgur.com/8y46BYK.png)

