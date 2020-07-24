.. _control:

Project Control
===============

Once a project folder is prepared, user can manage the project
via the project control ``droptctl``,
which is included in the Dr.Opt client package ``dropt-cli``.
To install it, simply run

.. code-block:: shell

   $ pip install dropt-cli


Basic Syntax
------------

Here is the basic syntax of ``droptctl``:

.. code-block:: shell

   $ droptctl -s ADDRESS -p PORT -t TOKEN CMD

* ``ADDRESS`` and ``PORT`` indicate which Dr.Opt server ``droptctl`` will connect to.
  If not given, `default Dr.Opt server <https://dropt.goedge.ai>`_ will be used.

* ``TOKEN`` is the unique identification of each user.
  It can be found on one's own **My account** page.

* ``CMD`` is the command to be sent.  Currently, two commands are supported:

  - create
  - resume


Create
------

.. code-block:: shell

   $ droptctl -t TOKEN create -c CONFIG_FILE

Create and run a new project based on config file ``CONFIG_FILE``.
The default config file is ``config.json``.


Resume
------

User may resume a project if interrupted.

.. code-block:: shell

   $ droptctl -t TOKEN resume

A prompt will show all ongoing projects and user selects one to resume.

.. code-block:: shell
   
   ? Which project would you like to resume?  (Use arrow keys)
     [project 120: dummy] progress: 2/100 (created at 2020-05-08T15:46:54.059234+00:00)
     [project 119: dummy] progress: 4/100 (created at 2020-05-08T15:46:26.824813+00:00)
   » [Project 75: func-eggholder] progress: 3/1000 (created at 2020-06-29T01:03:45.065417+00:00)
     [Project 76: func-eggholder] progress: 2/1000 (created at 2020-06-29T01:03:55.605235+00:00)  
