Advisor & Search Space
=======================


.. _advisor:

Advisor
-------

Dr.Opt supports the following advisors:

.. csv-table::
   :header-rows: 1
   :widths: 21, 79
   :file: ../tables/advisors.csv
   :delim: \


Anneal
^^^^^^

Arguments
    :optimize_mode: ``maximize`` (default) or ``minimize``

Example
    .. code-block:: json

       {
           "builtinTunerName": "Anneal",
           "classArgs": {"optimize_mode": "maximize"}
       }


Evolution
^^^^^^^^^

Arguments
    :optimize_mode: ``maximize`` (default) or ``minimize``
    :population_size: The initial size of the population

Example
    .. code-block:: json

       {
           "builtinTunerName": "Evolution",
           "classArgs": {
               "optimize_mode": "maximize",
               "population_size": 100
           }
       }


Grid Search
^^^^^^^^^^^

Arguments
    :None:

Config example
    .. code-block:: json

       {
           "builtinTunerName": "GridSearch"
       }


Random
^^^^^^

Arguments
    :None:

Config example
    .. code-block:: json

       {
           "builtinTunerName": "Random"
       }


TPE
^^^

Arguments
    :optimize_mode: ``maximize`` (default) or ``minimize``

Example
    .. code-block:: json

       {
           "tuner": {
               "builtinTunerName": "TPE",
               "classArgs": {"optimize_mode": "maximize"}
           }
       }


.. _searchspace:

Search Space
------------

Each parameter to search is assigned with certain space type.
Dr.Opt currently supports the following search space types:


choice
^^^^^^

Choose from a list of available options.

Format
    A list of of numbers or strings, e.g.,
    [0.1, 0.01, 0.001, 0.0001] or ["Adam", "SGD", "Adadelta"]

Example
    .. code-block:: json

       {
           "learning_rate": {
               "_type": "choice",
               "_value": [0.1, 0.01, 0.001, 0.0001]
           }
       }


randint
^^^^^^^

Choose a random integer within an interval.

Format
    [`lower_bound` (inclusive), `upper_bound` (exclusive)]

Example
    .. code-block:: json

       {
           "batch_size": {
               "_type": "randint",
               "_value": [8, 65]
           }
       }


uniform
^^^^^^^

Choose a number randomly from a uniform distribution on an interval.

Format
    [`lower_bound` (inclusive), `upper_bound` (exclusive)]

Example
    .. code-block:: json

       {
           "droptout_rate": {
               "_type": "uniform",
               "_value": [0.1, 0.5]
           }
       }


quniform
^^^^^^^^

Choose a number randomly from an interval descretized by a fixed step size.

Format
    [`lower_bound` (inclusive), `upper_bound` (exclusive), `step`]

Example
    .. code-block:: json

       {
           "input_size": {
               "_type": "quniform",
               "_value": [224, 417, 32]
           }
       }

    Note: In this example, the possible values are: 224, 256, 288, 320, ..., 384, 416.


normal
^^^^^^

Choose a number randomly from a normal discribution with
prescribed mean (:math:`\mu`) and standard deviation (:math:`\sigma`).

Format
    [:math:`\mu`, :math:`\sigma`]

Example
    .. code-block:: json

       {
           "dropout_rate": {
               "_type": "normal",
               "_value": [0.5, 0.1]
           }
       }


Support of Tuners/Search Space Types
------------------------------------

.. csv-table::
   :header-rows: 1
   :widths: 25, 15, 15, 15, 15, 15
   :file: ../tables/advisor_and_searchspace.csv
   :delim: \
