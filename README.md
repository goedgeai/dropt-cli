# dropt-cli
Dr.Opt is an ML model optimization service consisting of
- Hyper-parameter tuning tools
- WebUI for result visualization & analysis

A public Dr.Opt server is hosted on <https://dropt.goedge.ai>.

`dropt-cli` is the client application of Dr.Opt encapsulated
in a Python package.  To use it, users either run or wrap
the ML model in Python.



## Installation
### Prerequisites
- `Python>=3.6`
- `pip>=20.0.0`


### On Linux distro using APT
If running linux distribution such as Ubuntu,
one can perform the following commands for
the prerequisites.

```console
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install python3 python3-pip
$ sudo pip install --upgrade pip
```


### [Optional] Virtual environment
We recommend users to set up virtual environment
for `dropt-cli`.

- Install `virtualenv`
  ```console
  $ sudo pip install --upgrade virtualenv
  ```

- Create and activate virtual environment
  ```console
  $ virtualenv venv
  $ source venv/bin/activate
  ```

- Deactivate virtual environment
  ```console
  $ deactivate
  ```


### Download/Install the package
#### from PyPI
`dropt-cli` is hosted on [PyPI](https://pypi.org/project/dropt-cli/)
and can be installed via `pip`:

```console
pip install dropt-cli
```

#### from GitHub
If (1) the source code and/or examples are needed,
(2) wanting to try a development version,
one can download the package from the [GitHub repository](https://github.com/GoEdge-ai/dropt-cli).

- Download the source code
  ```console
  $ git clone https://github.com/GoEdge-ai/dropt-cli.git
  ```

- Install the package
  ```console
  $ cd dropt-cli
  $ pip install .
  ```

We also provide __wheel binary distribution__
and __source code archive__ on
<https://github.com/GoEdge-ai/dropt-cli/releases/latest>.
Simply click links on the page to download the files.

The `.whl` file is sufficient for installation.
The source code and examples are included in
the archive (`.zip` or `.tar.gz` files).

- Install the package from wheel binary distribution
  ```
  $ pip install [the filename of the wheel file]
  ```


## DrOpt Server
### Registration
- Open Dr.Opt server webpage (<https://dropt.goedge.ai/>) and click __Sign in__.
  ![DrOpt homepage](https://i.imgur.com/IZ7arvC.png?1)
- Select __Continue__ to start the registration.
  ![DrOpt sign-in page](https://i.imgur.com/4ShuboJ.png?1)
- Once the registration is approved, an email will be sent.


### Get an Access Token
- The link to the access token is found in __My Account__ page.
  ![token](https://i.imgur.com/QsUyxVH.png?1)
- Copy the __api token__ for later usage.



## Run a DrOpt Project
An optimization problem runs on the Dr.Opt service is called
a __project__.

We will use __an ML model tuning problem__
to illustrate the steps of running a project.


### Preparation
- Create a folder for your project.
- Two files are needed in the folder:
  - `model.py`: the Python code of the model you want to tune
  - `config.json`: the configuration of the project
  
  The names these two files are customizable.
- `model.py` should contain a function named `run()`:
  ```python
  def run(params):
      ...

      return result
  ```
  - `run()` recevies hyper-parameters of a model as a __dictionary__.
  - `result` should be a floating point number indicating the performance of
    the resulting model.
- Here is an example:
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
- `config.json` should include __metadata of the project__,
  the __default value of model hyper-parameters__ and
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
    __Note that the value of `model` should coincide
    with the filename of the model.__
  - `params`: default value of parameters
  - `search_space`: search space of hyper-parameters


### Create/Run a DrOpt Project
- Use script `droptctl` to create or resume a Dr.Opt project.
- Run the following command for the instruction of `droptctl`:
  ```console
  $ droptctl -h   
  usage: droptctl [-h] [-v] -t TOKEN [-s ADDRESS] [-p PORT] CMD ...

  Use command to control DrOpt project.

  optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -t TOKEN, --token TOKEN
                          user token
    -s ADDRESS, --server ADDRESS
                          server address (default: dropt.goedge.ai)
    -p PORT, --port PORT  port number

  commands:
    CMD
      create              create new project
      resume              resume an existing project

  Run "droptctl CMD -h" to learn more about a specific command.
  ```
- While there are default values for Dr.Opt server address and project config file,
  it suffices to pass only the __user token__ to `droptctl` in most cases.
- For example, simply run the following command to start a new DrOpt project:
  ```console
  $ droptctl -t [your token] create
  ```

### Resume a DrOpt Project

* To resume a project, run the following command under the project folder:

  ```console
  $ droptctl -t [your token] resume
  ```
* A prompt will list all project found in the local cache.
  User then select one to resume.
  ```console
  ? Which project would you like to resume?  (Use arrow keys)
    [project 120: dummy] progress: 2/100 (created at 2020-05-08T15:46:54.059234+00:00)
    [project 119: dummy] progress: 4/100 (created at 2020-05-08T15:46:26.824813+00:00)
  » [Project 75: func-eggholder] progress: 3/1000 (created at 2020-06-29T01:03:45.065417+00:00)
    [Project 76: func-eggholder] progress: 2/1000 (created at 2020-06-29T01:03:55.605235+00:00)                         
  ```


## Result Analysis
Once a project is created, its result will be presented on the Dr.Opt webpage.
![](https://i.imgur.com/tZLKzMV.png)
![](https://i.imgur.com/u96FW8D.png)
![](https://i.imgur.com/I3cNOEe.png)



## Examples
One can find more examples about Dr.Opt project in folder `examples`.

## About
* The modules under [src/dropt/client](./src/dropt/client) (`endpoint.py`, `exception.py`, `interface.py`, `objects.py`, `requestor.py`, `resource.py`) are modified from [sigopt-python](https://github.com/sigopt/sigopt-python), which is under the MIT license:
```
The MIT License (MIT)

Copyright (c) 2014-2015 SigOpt Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

* The implementation of tuner algorithms are modified from [NNI (Neural Network Intelligence)](https://github.com/microsoft/nni), which is under the MIT license:
```
Copyright (c) Microsoft Corporation.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
