.. _quickstart:

Quickstart
==========

Installation
------------

One can easily install the client package with pip

.. code:: shell

   pip install dropt-cli


Registration/Get Access Token
-----------------------------
1. Go to `Dr.Opt server webpage <https://dropt.goedge.ai>`_ and click ``Sign in``.

.. image:: https://i.imgur.com/IZ7arvC.png?1
   :alt: Dr.Opt Homepage
   :align: center

2. Click ``Continue`` to start the registration.
   User will be notified via email once the registration is approved.

.. image:: https://i.imgur.com/4ShuboJ.png?1
   :alt: Registration
   :align: center

3. In ``My Account`` page click ``My tokens``

.. image:: https://i.imgur.com/QsUyxVH.png?1
   :alt: Access token
   :align: center

4. Copy the ``api token`` for later usage.


Download and run the examples
-----------------------------

1. Download our examples from GitHub:

.. code:: shell

   git clone https://github.com/GoEdge-ai/dropt-example

2. Move to the directory of a trial example:

.. code:: shell

   cd dropt-example/trials/func-eggholder

3. Install required Python package:

.. code:: shell

   pip install -r requirements.txt

4. Create and run a new DrOpt project with our controller script,
   in which ``TEKON`` is the access token of your account:

.. code:: shell

   droptctl -t TOKEN create


Review Project Result
---------------------

Log in `Dr.Opt server <https://dropt.goedge.ai>`_ and review the result of your project.
