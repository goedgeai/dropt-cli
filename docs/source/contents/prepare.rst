.. _prepare:

Prepare A Project
=================

In Dr.Opt, a parameter optimization task is called a **project**.
Before starting a new project, user needs to prepare
a project folder containing all necessary files.
Here we will brief how it is done.


Folder Structure
----------------

The following diagram depicts the minimal structure of a project folder:

.. code-block::

   MyProject
   ├── config.json
   └── mymodel.py

* ``mymodel.py``: A Python file for the model to be tuned
* ``config.json``: A JSON file describing the configuration of the project

Note that the names of both files are customizable.


mymodel.py
----------

The Python file should contain the following function:

.. code-block:: python

   def run(params):
       ...

       return metric

* The input ``params`` represents the hyper-parameter configuration for the model.
* The output ``metric`` measures the performance, such as accuracy or latency, of the model.

Here is an example how ``run`` should work:

.. code-block:: python

   >>> from mymodel import run
   >>> params = {
   ...     "max_depth": 10,
   ...     "gamma": 0.25,
   ...     "alpha": 0.5,
   ...     "learning_rate": 0.001,
   ...     "subsample": 0.75,
   ...     "colsample": 0.75
   ... }
   >>> run(params)
   0.732


config.json
-----------

We consider an example config file:

.. code-block:: json

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

Three main sections should be included in the JSON file:

config
    This project

params

search_space
