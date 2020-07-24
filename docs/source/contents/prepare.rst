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


.. _mymodel:

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
^^^^^^

This section contains config options of the project,
which includes:

experimentName (string)
    * Name of the project, which will be shown on the Dr.Opt webpage

maxTrialNum (number/integer)
    * The maximum number of trials of this project

maxExecDuration (number/integer)
    * The expected maximal execution time of the project in `hour` (default: 12 hrs)
    * If the experiment time exceeds the **maxExecDuration**,
      the project state will change to "finish" and
      inpcomplete suggestions will be discarded.

parentProject (string)
    * The parent project of the current one
    * (Coming in the future)
      The newly created project can inherent the properties of the **parentProject**
    * Just set to ``None`` for now

model (string)
    * The Python file of the model to be tuned (without file extension)

mode (string)
    * The optimization mode of the project.
      It can be ``max`` (default) or ``min``.

updatePeriod (number/integer)
    * The update period of the webpage (in `second`)

tuner (object)
    * parameter search algorithm
    * See page :ref:`advisor` for detail


params
^^^^^^

This section consists of default hyper-parameter of the model.
Its format should conincide with that of input of ``run`` (see section :ref:`mymodel`).


search_space
^^^^^^^^^^^^

This section describes the search space.
Please read page :ref:`searchspace` for detail.
