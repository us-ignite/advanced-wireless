Application commands
====================

The application uses ``fabric`` to interact with the ``local development`` and the ```production`` build.

Some commands are required to be run inside or outside the the ``VM``.


Reset the local database
------------------------

While the models are still being defined it is useful to reset the database for the vm. The following command must be run **inside** the vm::

    fab reset_local_db

This command will drop the existing database and re create it by running ``syncdb``.


Runnning the test suite
-----------------------

The test suite is processed by running the following command **inside** the ``VM``::

    fab test


Deploy the application to Heroku
--------------------------------

Deploying the application to heroku requires a set of steps.

The command verifies that all the changes have been pushed to ``origin`` to avoid deploying a set of commits to the ``production`` origin. As well runs any update required on the database.

This command must be run **ouside** the ``VM``::

    fab production deploy


Running Django console in heroku
--------------------------------

If a ``Django`` console is required in the application this can be achieved by runnig **inside** the ``VM``::

    fab production shell


Loading initial fixtures
------------------------

A single command has been provided to load the initial fixtures in the remote server. The command must be executed **outside** the VM.

    fab production load_fixtures

