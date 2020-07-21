Project Control
===============

User can **create** or **resume** a project with our controller script ``droptctl``.


Basic Syntax
------------

``droptctl`` admits the following syntax:

.. code:: shell

   droptctl -s ADDRESS -p PORT -t TOKEN CMD

- ``ADDRESS`` and ``PORT`` indicate which Dr.Opt server controller will connect.
  If not given, controller will use the `default Dr.Opt server <https://dropt.goedge.ai>`_.

- ``TOKEN`` is the unique identification of each user. It can be found on one's own **My account** page.

- ``CMD`` can be one of the following commands
  - `create`: create and run a new project
  - `resume`: resume and run an existing project; a prompt will let user select the project to resume
