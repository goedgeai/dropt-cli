# Dr.Opt Client Readme

Dr.Opt is a ML model optimization service, which includes automatic hyper-parameter tuning tools and provides a WebUI to visualize tuning results & analysis.


# Getting started

## Prerequisites
### Install Dr.Opt client package
```
pip install dropt
```

## Create an account and get a token
### Go to [Dropt Website](https://dropt-beta.nctu.me) and create an account by "New Customer"
> current DrOpt v2 beta address: dropt-beta.nctu.me

![](https://i.imgur.com/jVBDmRM.png)


### Get the access token

After creating the account, click "My Account" -> "My tokens"

![](https://i.imgur.com/FOjAhgY.png)


The string on the "My tokens" page is your dropt client token. (The USER_TOKEN in the following sample code)

![](https://i.imgur.com/XCWFp2i.png)


## How to apply the optimization with Dr.Opt

### (1) Have an training code that can set the hyperparameters by the arguments
* For instance, the function 'train' will execute the training process and return the results
```python
result = train(
            max_depth=10, 
            gamma=0.25, 
            subsample=0.75, 
            colsample=0.75, 
            alpha=0.5, 
            learn_rate=0.001
         )
"""
result = {'acc': 0.932, 'latency': 0.43}
"""
```

### (2) Insert Dr.Opt API code in the original training program

#### Import dropt package
```python
import dropt
```

#### Define API token for authorization
```python
conn = dropt.Connection(client_token=[USER_TOKEN], server_ip=[DROPT_IP])
```

#### Load the configuration file and create a new project
* As for the configuration file, please refer to this config README
```python
project = conn.projects().create(
   config = dropt.load_config_file([CONFIG_FILE])
)
```

#### Get suggestions from DrOpt
```python
suggestion = conn.projects(project_id).suggestions().create()
sugt_id = suggestion.suggest_id
sugts = suggestion.assignments
"""
    The return object "suggestion.assignments" is a dict that contains values of each paramter.
    The sugt_id will be used when report the result.
    
    sugts = {
        'filter1': '64',
        'filter2': '32', 
        'ksize': '5',
        'learn_rate': '0.001',
        'hidint': '100'
    }
    
    (please note that the values are strings)
"""
```

#### Report the training result to DrOpt
```python
conn.projects(project_id).validations().create(
    suggest_id = sugt_id,
    value = float(metric),              # metric (a single value)
    value_detail = json.dumps(metric)   # details of metric (json string)
)
```

### A complete example

```python
import dropt

# Define API token for authorization
conn = dropt.Connection(client_token=[USER_TOKEN], server_ip=[DROPT_IP])

# Create DrOpt project
project = conn.projects().create(
   config = dropt.load_config_file([CONFIG_FILE])
)

# Get project id that returned from DrOpt
project_id = project.project_id
project_trial = project.trial

# Run the optimization loop
for i in range(project_trial):
    # Retrieve hyperparamaters from DrOpt
    suggestion = conn.projects(project_id).suggestions().create()
    sugt_id = suggestion.suggest_id
    sugts = suggestion.assignments
    
    """
    The return object "suggestion.assignments" is a dict 
    (please note that the values are strings)
    
    sugts = {
        'filter1': '64',
        'filter2': '32', 
        'ksize': '5',
        'learn_rate': '0.001',
        'hidint': '100'
    }
    """
    
    # user's training fuction
    metric = train(filter1=['filter1'], filter2=['filter2'], ... )
    
    """
    if metric is a dict:
    metric = {
        'acc': 0.94
        'latency': 10
    }
    """
    
    # report result to Dr.Opt
    conn.projects(project_id).validations().create(
     suggest_id = sugt_id,
     value = float(metric),              # metric (a single value)
     value_detail = json.dumps(metric)   # details of metric (json string)
    )
```

## Client code examples

The tuning samples is located in ```examples```. As for the details of each training example, please refer to the example README.

## Result Analysis

When the training is done, the results and the analysis will be shown on the project list.

![](https://i.imgur.com/tZLKzMV.png)

![](https://i.imgur.com/u96FW8D.png)

![](https://i.imgur.com/I3cNOEe.png)


