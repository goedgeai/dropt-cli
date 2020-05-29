# dropt-cli
DrOpt is an ML model optimization service consisting of the following
parts:
- Hyper-parameter tuning tools
- WebUI for result visualization & analysis

A public DrOpt server is hosted on <https://dropt.neuralscope.org>.

`dropt-cli` is the client application of DrOpt service encapsulated
as a Python package; users need to either run their ML model in Python
or to wrap their ML model in Python at least.



## Installation
### Prerequisites
We have tested `dropt-cli` in the following environments:
- `Python>=3.6`
- `pip>=20.0.0`


### On Linux distro using APT
If running linux distribution such as Ubuntu,
one can perform the following commands to meet
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
A repository of `dropt-cli` is hosted on GitHub:
<https://github.com/NeuralScope/dropt-cli>.

#### with Git
One can download the source code from GitHub and
install the package.

- Download the source code
  ```console
  $ git clone https://github.com/NeuralScope/dropt-cli
  ```

- Install the package
  ```console
  $ cd dropt-cli
  $ pip install .
  ```

#### without Git
Alternatively, we provide __wheel binary distribution__
and __source code archive__ on
<https://github.com/NeuralScope/dropt-cli/releases/latest>.
Simply click links on the page to get the files.

The `.whl` file is sufficient for installing `dropt-cli`.
The source code and examples of `dropt-cli` are included in
the source code archive (`.zip` or `.tar.gz` files).

- Install the package from wheel binary distribution
  ```
  $ pip install [the filename of the wheel file]
  ```


## DrOpt Server
### Registration
- Open DrOpt server webpage (<https://dropt.neuralscope.org/>) and click __Sign in__.
  ![DrOpt homepage](https://i.imgur.com/IZ7arvC.png?1)
- Select __Continue__ to start the registration.
  ![DrOpt sign-in page](https://i.imgur.com/4ShuboJ.png?1)
- Once the registration is approved, a email will be sent.


### Get an Access Token
- The link to the access token is found in __My Account__ page.
  ![token](https://i.imgur.com/QsUyxVH.png?1)
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
  usage: droptctl [-h] -t TOKEN [-s SERVER] [-c CONFIG] [CMD]

  Create DrOpt projects.

  positional arguments:
    CMD                   the action that will be executed by droptctl

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

### Resume a DrOpt Project (will be available soon)

> The `resume` function will be available after the coming server maintenance. Please stay tuned to our announcement for updates!

* To resume a project, run the following command under the project folder:

  ```console
  $ droptctl resume -t [your token]
  ```
* After executing `droptctl resume`, if any project progress file is found under the project folder, there will be a prompt that provides a resumable project list.

  ```console
  ? Which project would you like to resume?  (Use arrow keys)
    [project 122] name: dummy, progress: 4, create_time: 2020-05-08 16:11:10
  » [project 121] name: dummy, progress: 1, create_time: 2020-05-08 16:10:05
    [project 120] name: dummy, progress: 2, create_time: 2020-05-08 15:46:54
    [project 119] name: dummy, progress: 4, create_time: 2020-05-08 15:46:26
  ```

* If `droptctl` can't found any progress file, user can manually input the `project_id`.
* The `project_id` can be found on the WebUI (project sidebar ➔ Properties).

  ```console
  ! The project history directory does not exist.

  ? Would you like to specify a project_id?  Yes
  ? The project_id you would like to resume: 123
  ```



## Result Analysis
Once a project is created, its result will be presented on the DrOpt webpage.
![](https://i.imgur.com/tZLKzMV.png)
![](https://i.imgur.com/u96FW8D.png)
![](https://i.imgur.com/I3cNOEe.png)



## Examples
One can find more examples about DrOpt project in folder `examples`.

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
