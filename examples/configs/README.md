# Dr.Opt config README

To perform optimization with Dr.Opt, besides insert API code, the user also needs to set the experiment and searching space by a configuration file. which is defined in JSON format.

This README provides the information of Dr.Opt config file and the available options.

## 1. Give the experiment settings

The experiment settings must include:

#### experimentName
* Name of the project, which will be shown on the Dr.Opt webpage.
#### tuner/advisor
* Name of the tuner/advisor. Every project must specify a tuner or a advisor.
#### maxTrialNum
* The number of trials of this project. For instance, if maxTrialNum=50, then Dr.Opt will give 50 suggestions for this project.
#### maxExecDuration (optional)
* The expected maximal execution time of the project. (unit: hour)
* If the experiment time exceeds the maxExecDuration, Dr.Opt will set the project state as finish and discard the incomplete suggestions.

#### parentProject
* The new created project can inherit the properties of the parentProject
* The inherit function will be provided on the DrOpt website (not available yet)
* Just set to `None` for now

#### model
* The used model of the project. Can set any value (string).
* (It is also designed for the inherit function)

#### updatePeriod
* The update period of the webpage. (unit: minute)
* Could just leave it blank now.

### Sample
```python
"config":{
    "experimentName": "car_detection",
    "maxExecDuration": "30h",
    "maxTrialNum": 50,
    "parentProject": "my_parent",
    "model": "YOLOv3",
    "updatePeriod": 60,
    "tuner": {
      "builtinTunerName": "TPE",
      "classArgs":{
        "optimize_mode": "maximize"
      }
    }
```

## 2. Give the searching space
The search space indicates the paramters that the user would like to search. The search space should include the name and the range(distribution).

### Sample
```
{
    "dropout_rate":{"_type":"uniform","_value":[0.5, 0.9]},
    "batch_size": {"_type":"choice", "_value": [1, 4, 8, 16, 32]},
    "learning_rate":{"_type":"choice","_value":[0.0001, 0.001, 0.01, 0.1]}
    "optimizer":{"_type":"choice", "_value":["SGD", "Adadelta", "Adagrad", "Adam", "Adamax"]}
}
```
Please note that each tuner supports different kinds of searching space. As for the details of availability of each search space type, please refer to [NNI search space document](https://nni.readthedocs.io/en/latest/Tutorial/SearchSpaceSpec.html#search-space-types-supported-by-each-tuner).

## 3. Combine experiment config and search space
Here is a complete sample:
```
{
    "config":{
      "experimentName": "test",
      "maxExecDuration": "1h",
      "maxTrialNum": 10,
      "tuner": {
        "builtinTunerName": "TPE",
        "classArgs":{
          "optimize_mode": "maximize"
        }
      },
      "parentProject": "my_parent",
      "model": "my_network",
      "updatePeriod": 600
    },
    "search_space":{
      "dropout_rate":{"_type":"uniform","_value":[0.5, 0.9]},
      "lr":{"_type":"choice", "_value":[0.1, 0.01, 0.001, 0.0001]},
      "optimizer":{"_type":"choice", "_value":["SGD", "Adadelta", "Adagrad", "Adam", "Adamax"]}
    }
}
```

## Current available tuners

* Anneal​
* Naïve Evolution​
* GP Tuner​
* Grid Search​
* Random​
* TPE

As for the details of the tuners, please refer to the [NNI tuner document](https://github.com/microsoft/nni/blob/master/docs/en_US/Tuner/BuiltinTuner.md#Anneal).


<!--
### Anneal​
> Built-in Tuner Name: Anneal
#### classArgs
* optimize_mode
    * maximize or minimize, default = maximize
### Batch Tuner​
> Built-in Tuner Name: BatchTuner
#### classArgs
* (None)
### Naïve Evolution​
> Built-in Tuner Name: Evolution
#### classArgs
* optimize_mode
    * maximize or minimize, default = maximize
* population_size
    * int value (should > 0), optional, default = 20
    * the initial size of the population (trial num) in evolution tuner
### GP Tuner​
> Built-in Tuner Name: GPTuner
#### classArgs
* optimize_mode
    * maximize or minimize, default = maximize
* utility ('ei', 'ucb' or 'poi', optional, default = 'ei')
    * The kind of utility function (acquisition function)
* kappa (float, optional, default = 5) 
    * Used by utility function 'ucb'
#### Note
This tuner only support numerical values.
#### Grid Search​
#### Metis Tuner​
#### Random​
#### SMAC​
#### TPE
arguments
* optimize_mode (maximize or minimize, optional, default = maximize)
-->