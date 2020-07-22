.. _quickstart:

Quickstart
==========

Here we illustrate how to one can create and run a Dr.Opt project
based on `our trial examples <https://github.com/GoEdge-ai/dropt-example>`_.


Prerequisites
-------------

Before starting, make sure the following things are installed in your system:

* Python 3.6 or newer
* pip


Registration/Get Access Token
-----------------------------
1. Go to `Dr.Opt server webpage <https://dropt.goedge.ai>`_ and click ``Sign in``.

.. image:: https://i.imgur.com/IZ7arvC.png?1
   :alt: Dr.Opt Homepage
   :align: center

2. Click ``Continue`` and finish the registration.
   User will be notified via email once the registration is approved.

.. image:: https://i.imgur.com/4ShuboJ.png?1
   :alt: Registration
   :align: center

3. In ``My Account`` page click ``My tokens``

.. image:: https://i.imgur.com/QsUyxVH.png?1
   :alt: Access token
   :align: center

4. Copy the ``api token`` for later use.


Download and run the examples
-----------------------------

1. Download our examples from GitHub:

.. code-block:: shell

   $ git clone https://github.com/GoEdge-ai/dropt-example.git

2. Move to the directory of a trial example:

.. code-block:: shell

   $ cd dropt-example/trials/func-eggholder

3. Install required Python package:

.. code-block:: shell

   $ pip install -r requirements.txt

4. Create and run a new Dr.Opt project with our control script,
   in which ``TEKON`` is the access token of your account:

.. code-block:: shell

   $ droptctl -t TOKEN create


Inspect Project Result
----------------------

Inspect the result on the `Dr.Opt server webpage <https://dropt.goedge.ai>`_.
