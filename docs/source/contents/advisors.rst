.. _advisors:

Advisors
========

Dr.Opt supports the following advisors:

.. csv-table::
   :header-rows: 1
   :widths: 21, 79
   :file: ../tables/advisors.csv
   :delim: \

Usage
-----

Anneal
^^^^^^

Arguments
"""""""""

Config example
""""""""""""""


Evolution
^^^^^^^^^

Arguments
"""""""""

Config example
""""""""""""""


Gaussian Process
^^^^^^^^^^^^^^^^

Arguments
"""""""""

Config example
""""""""""""""


Grid Search
^^^^^^^^^^^

Arguments
"""""""""

Config example
""""""""""""""


Random
^^^^^^

Arguments
"""""""""

Config example
""""""""""""""


TPE
^^^

Arguments
"""""""""

* optimize_mode: **maximize** or **minimize** (default: maximize)

Config example
""""""""""""""

.. code-block:: json

   {
       "tuner": {
           "builtinTunerName": "TPE",
           "classArgs": {"optimize_mode": "maximize"}
       }
   }
