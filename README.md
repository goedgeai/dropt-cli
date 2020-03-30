# dropt-cli
DrOpt is an ML model optimization service consisting of the following
parts:
- Hyper-parameter tuning tools
- WebUI for result visualization & analysis

A public DrOpt server is hosted on <https://dropt.neuralscope.org>.

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


### Download the Package
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


### Install the Package
Prepend `sudo` to the following commands if necessary.
- Update `pip`:
  ```console
  $ pip install --upgrade pip
  ```
- __[optional]__ Use virtual environment:  
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



## DrOpt Server
### Registration
- Open DrOpt server webpage (<https://dropt.neuralscope.org/>) and click __Sign in__.
  ![DrOpt homepage](https://i.imgur.com/IZ7arvC.png)
- Select __Continue__ to start the registration.
  ![DrOpt sign-in page](https://i.imgur.com/4ShuboJ.png)
- Once the registration is approved, a email will be sent.


### Get an Access Token
- The link to the access token is found in __My Account__ page.
  ![token](https://i.imgur.com/QsUyxVH.png)
- Copy the __api token__ (a string) for later usage.



## Run a DrOpt Project
A DrOpt project uses the DrOpt service to solve an optimization problem.

We will use __finding a best hyper-parameter combination for an ML model__
to illustrate the steps of preparing and running a DrOpt project.


### Preparation
- Create a folder for your DrOpt project.
- Two files are needed in the folder:
  - `model.py`: the Python code of the model you want to optimize
  - `config.json`: the configuration of the project
  
  You can choose different names for these two files.
- `model.py` should contain a function named `run()`:
  ```python
  def run(params):
      ...

      return result
  ```
  - `run()` recevies all required parameters of a model
    as a __Python dictionary__, which includes the hyper-parameters to be tuned.
  - `result` should be a floating point number indicating the performance of
    the resulting model.
- Here is an example of calling `run()`:
  ```python
  params = {"max_depth": 10,
            "gamma": 0.25,
            "subsample": 0.75,
            "colspample": 0.75,
            "alpha": 0.5,
            "learn_rate": 0.001}
  acc = run(params)
  """
  acc = 0.732
  """
  ```
- `config.json` should include __metadata of your DrOpt project__,
  the __default value of model parameters__ and
  the __search space of model hyper-parameters__.
- Here is an example of `config.json` for an XGBoost classification model:
  ```
  {
      "config": {
          "experimentName": "titanic-xgboost",
          "maxExecDuration": "1h",
          "maxTrialNum": 10,
          "parentProject": "None",
          "model": "model",
          "updatePeriod": 60,
          "tuner": {
              "builtinTunerName": "TPE",
              "classArgs": {"optimize_mode": "maximize"}
          }
      },

      "params": {
          "booster": "gbtree",
          "verbosity": 0,
          "base_score": 0.5,
          "colsample_bylevel": 1,
          "n_estimators": 50,
          "objective": "binary:logistic",
          "max_depth": 5,
          "gamma": 0.2,
          "subsample": 0.8,
          "colsample-bytree": 0.8,
          "lambda": 1,
          "alpha": 0.25,
          "eta": 0.01,
          "min_child_weight": 1.0
      },
                  
      "search_space": {
          "max_depth": {"_type": "randint", "_value": [1, 5]},
          "gamma": {"_type": "uniform", "_value": [0.1, 1.0]},
          "subsample": {"_type": "uniform", "_value": [0.1, 1.0]},
          "colsample_bytree": {"_type": "uniform", "_value": [0.1, 1.0]},
          "alpha": {"_type": "uniform", "_value": [0.1, 1.0]},
          "eta": {"_type": "uniform", "_value": [0.1, 1.0]}
      }
  }
  ```
  - `config`: metadata of the project  
    __Note that the value of field `model` here should coincide
    with the filename of the Python model code.__
  - `params`: default value of parameters
  - `search_space`: search space of hyper-parameters


### Create/Run a DrOpt Project
- User can use script `droptctl` to create and run a DrOpt project.
- Run the following command for user instructions of `droptctl`:
  ```console
  $ droptctl -h
  usage: droptctl [-h] -t TOKEN [-s SERVER] [-c CONFIG]

  Create DrOpt projects.

  optional arguments:
    -h, --help            show this help message and exit
    -t TOKEN, --token TOKEN
                          user token
    -s SERVER, --server SERVER
                          server address (default: dropt.neuralscope.org/)
    -c CONFIG, --config CONFIG
                          config file (default: ./config.json)
  ```
- Since there are default values for DrOpt server address and project config file,
  it suffices to pass the __user token__ to `droptctl` in most cases.
- In aforementioned example, simply run the following command
  under the project folder to start a new DrOpt project:
  ```console
  $ droptctl -t [your token]
  ```



## Result Analysis
Once a project is created, its result will be presented on the DrOpt webpage.
![](https://i.imgur.com/tZLKzMV.png)
![](https://i.imgur.com/u96FW8D.png)
![](https://i.imgur.com/I3cNOEe.png)



## Examples
One can find more examples about DrOpt project in folder `examples`.
