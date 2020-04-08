# Dr.Opt config README

To perform optimization with Dr.Opt, besides insert API code, the user also needs to set the experiment and searching space by a configuration file, which is defined in JSON format.

This README provides the information of Dr.Opt config file and the available options.

#### The config file should contain 3 parts:
* experiment settings
* parameters
* searching space

The following sections will introduce the requirements and more details for each part.

## 1. Give the experiment settings

The experiment settings must include:

#### experimentName
* Name of the project, which will be shown on the Dr.Opt webpage.
#### maxTrialNum
* The number of trials of this project. 
* For instance, if maxTrialNum=50, then Dr.Opt will give 50 suggestions for this project.
#### maxExecDuration
* The expected maximal execution time of the project. (unit: hour)
* If the experiment time exceeds the maxExecDuration, Dr.Opt will set the project state as finish and discard the incomplete suggestions.
* Default: 12 hr

#### parentProject
* Just set to `None` for now
* In the future version,
    * the newly created project can inherent the properties of the parentProject
    * the inherit function will be provided on the DrOpt website (not available yet)

#### model
* The Python code of the training program that you want to optimize.
    * e.g. [mnist.py](../trials/mnist-pytorch/mnist.py) in the [mnist-pytorch example](../trials/mnist-pytorch)
    * see the `"model": "mnist"` in the following example:
```
    "config": {
        "experimentName": "mnist-pytorch",
        "maxExecDuration": "1h",
        "maxTrialNum": 10,
        "parentProject": "None",
        "model": "mnist",
        "updatePeriod": 60,
        "tuner": {
            "builtinTunerName": "TPE",
            "classArgs": {"optimize_mode": "minimize"}
        }
    }
```
* It should contain a function named `run()`
```python
def run(params):
    ...

    return result
```
* `run()` receives all required parameters of a model as a Python dictionary, which includes the hyper-parameters to be tuned
* `result` should be a floating-point number indicating the performance of the resulting model (e.g. accuracy)

#### mode
* The optimization mode of the project (`max` or `min`).
* Default: `max`

#### updatePeriod
* The update period of the webpage. (unit: second)
* Just set it to an arbitrary integer right now. (e.g. 1)

#### tuner/advisor
* Name of the tuner/advisor(tuning algorithm). Every project must specify an tuner or a advisor.
> Please refer to [Tuner & Search space README](TUNER_AND_SEARCH_SPACE.md) to get more information about the usage of tuners.

### Example
```
"config": {
        "experimentName": "titanic-xgboost",
        "maxExecDuration": "1h",
        "maxTrialNum": 10,
        "parentProject": "None",
        "mode": "max",
        "model": "xgb",
	    "updatePeriod": 1,
        "tuner": {
            "builtinTunerName": "TPE",
            "classArgs": {"optimize_mode": "maximize"}
        }
    }
```

## 2. Give the parameters (& arguments)
Define the parameters and arguments that needed by the training function, which specify the default values.

### Example
This is the parameter list of the [mnist-pytorch example](../trials/mnist-pytorch).
```
"params": {
    "batch_size": 64,
    "test_batch_size": 1000,
    "epochs": 14,
    "lr": 1.0,
    "gamma": 0.7,
    "no_cuda": false,
    "seed": 1,
    "log_interval": 10,
    "save_model": false,
    "hidden_size": 128
}
```

## 3. Give the searching space
The search space indicates the paramters that the user would like to search. The search space should include the parameter names, types and values (choice, range, or distribution).

> As for the details of how to define a search space, please refer to [Tuner & Search space README](TUNER_AND_SEARCH_SPACE.md).

### Example
* Below is the search space of [imagenet-pytorch example](../trials/imagenet-pytorch).
```
"search_space": {
    "epochs": {"_type": "choice", "_value": [10, 20, 40, 80]},
    "batch_size": {"_type": "choice", "_value": [32, 64, 128, 256]},
    "lr": {"_type": "choice", "_value": [0.1, 0.01, 0.001, 0.0001]},
    "momentum": {"_type": "choice", "_value": [0.1, 0.3, 0.5, 0.7, 0.9]},
    "weight_decay": {"_type": "choice", "_value": [0.01, 0.001, 0.0001, 0.00001]}
}

```


Please note that each tuner supports different kinds of searching space. As for the availability of each search space type, please refer to [Tuner & Search space README](TUNER_AND_SEARCH_SPACE.md).

## 4. Combine experiment settings, parameter list, and the search space

A Dr.Opt config file should be in JSON format and includes 3 objects: `config`, `params` and `search_space`. 

Here is a complete Dr.Opt config example:
```
{
    "config": {
        "experimentName": "mnist-pytorch",
        "maxExecDuration": "1h",
        "maxTrialNum": 10,
        "parentProject": "None",
        "model": "mnist",
        "updatePeriod": 60,
        "tuner": {
            "builtinTunerName": "TPE",
            "classArgs": {"optimize_mode": "minimize"}
        }
    },

    "params": {
        "batch_size": 64,
        "test_batch_size": 1000,
        "epochs": 14,
        "lr": 1.0,
        "gamma": 0.7,
        "no_cuda": false,
        "seed": 1,
        "log_interval": 10,
        "save_model": false,
        "hidden_size": 128
    },

    "search_space": {
        "batch_size": {"_type": "choice", "_value": [16, 32, 64, 128]},
        "hidden_size": {"_type": "choice", "_value": [128, 256, 512, 1024]},
        "lr": {"_type": "choice", "_value" :[0.0001, 0.001, 0.01, 0.1]},
        "gamma": {"_type": "uniform", "_value": [0, 1]}
    }
}
```

Please note that the config file also needs to be placed at the same directory with your training program. For instance, the directory that executes a Dr.Opt project would look like:
```
.
├── config.json         // configuration file
└── xgb.py              // training program
```
