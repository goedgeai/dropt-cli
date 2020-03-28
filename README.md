# dropt-cli
## Overview
DrOpt is an ML model optimization service consisting of the following
parts:
- Hyper-parameter tuning tools
- WebUI for result visualization & analysis

A public DrOpt server is on <https://dropt.neuralscope.org>.

`dropt-cli` is the client application of DrOpt service encapsulated
as a Python package.  As a result, it requires users either to
run their ML model or to wrap their ML model in Python.



## Installation
### Prerequisites
We have tested `dropt-cli` in the following environments:
- `Python>=3.5`
- `pip>=20.0.0`

Other prerequisites will be taken care of by `pip` when
installing the package.


### Download the package
A repository of `dropt-cli` is hosted on GitHub:
<https://github.com/NeuralScope/dropt-cli>.
Please use `git` to download the package:

```console
$ git clone https://github.com/NeuralScope/dropt-cli
```

Since the version of the package is determined by its Git metedata,
the package downloaded without `git` __cannot__ be installed via `pip`.

> __Todo:__ We will provide _wheel binary distribution_
> as an alternative in the future.


### Install the package
Prepend `sudo` to the following commands if necessary.
- Update `pip`:
  ```console
  $ pip install --upgrade pip
  ```
- Use virtual environment [optional]:  
  We recommend user to install and use `dropt-cli` in a
  __virtual environment__.
  ```console
  $ pip install --upgrade virtualenv
  $ virtualenv venv
  $ source venv/bin/activate
  ```
- Install `dropt-cli`:
  ```console
  $ cd dropt-cli
  $ pip install .
  ```



## DrOpt server
### Registration
- Open DrOpt server webpage (<https://dropt.neuralscope.org/>) and click __Sign in__.
  ![DrOpt homepage](https://i.imgur.com/IZ7arvC.png)
- Select __Continue__ to start the registration.
  ![DrOpt sign-in page](https://i.imgur.com/4ShuboJ.png)
- Once the registration is approved, a email will be sent.


### Get an access token
- The link to the access token is found in __My Account__ page.
  ![token](https://i.imgur.com/QsUyxVH.png)
- The __api token__ is a string. Copy it for later usage.



## Run DrOpt service
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
import dropt.client as dropt_cli
```

#### Define API token for authorization
```python
conn = dropt_cli.Connection(client_token=[USER_TOKEN], server_ip=[DROPT_IP])
```

#### Load the configuration file and create a new project
* As for the configuration file, please refer to the [Dr.Opt config README](examples/configs/).
```python
project = conn.projects().create(
   config = dropt_cli.load_config_file([CONFIG_FILE])
)
```

#### Get suggestions from Dr.Opt
```python
suggestion = conn.projects(project_id).suggestions().create()
sugt_id = suggestion.suggest_id
sugts = suggestion.assignments
"""
    The return object "suggestion.assignments" is a dict that contains values of each paramter.
    The sugt_id will be used when report the result.
    
    sugts = {
        'filter1': 64,
        'filter2': 32, 
        'ksize': 5,
        'learn_rate': 0.001,
        'hidint': 100
    }
"""
```

#### Report the training result to Dr.Opt
```python
conn.projects(project_id).validations().create(
    suggest_id = sugt_id,
    value = float(metric),              # metric (a single value)
    value_detail = json.dumps(metric)   # details of the metric (JSON string)
                                        # e.g. metric = {'acc': 0.927, 'latency':8.43}
                                        #      convert the dict to a str by json.dumps()
)
```

### A complete example

```python
import dropt.client as dropt_cli

# Define API token for authorization
conn = dropt_cli.Connection(client_token=[USER_TOKEN], server_ip=[DROPT_IP])

# Create Dr.Opt project
project = conn.projects().create(
   config = dropt_cli.load_config_file([CONFIG_FILE])
)

# Get project id that returned from Dr.Opt
project_id = project.project_id
project_trial = project.trial

# Run the optimization loop
for i in range(project_trial):
    # Retrieve hyperparamaters from Dr.Opt
    suggestion = conn.projects(project_id).suggestions().create()
    sugt_id = suggestion.suggest_id
    sugts = suggestion.assignments
    
    """
    The return object "suggestion.assignments" is a dict
    
    sugts = {
        'filter1': 64,
        'filter2': 32, 
        'ksize': 5,
        'learn_rate': 0.001,
        'hidint': 100
    }
    """
    
    # user's training fuction
    metric = train(filter1=['filter1'], filter2=['filter2'], ... )
    
    """
    assume that the metric is a dict:
    metric = {
        'acc': 0.94
        'latency': 10
    }
    """
    
    # report result to Dr.Opt
    conn.projects(project_id).validations().create(
     suggest_id = sugt_id,
     value = metric['acc'],              # metric (a single value)
     value_detail = json.dumps(metric)   # details of metric (json string)
    )
```

## Client code examples

The tuning samples is located in [examples](examples/). As for the details of each training example, please refer to the example README.

## Result Analysis

When the training is done, the results and the analysis will be shown on the project list.

![](https://i.imgur.com/tZLKzMV.png)

![](https://i.imgur.com/u96FW8D.png)

![](https://i.imgur.com/I3cNOEe.png)


