Bootstraping the application
============================

The application has been architectured to run remotely using Heroku, and locally using Vagrant.


Running locally
---------------

The application requires Vagrant setup, and a provisioner installed in the local machine. (VirtualBox being the easiest provisioner you can get hold of).

Once the pre-requisites have been installed the application can be started with the following command::

  vagrant up

.. note::

   The provisioning will take a while, since it needs to get a copy of the OS box and install any packages required.

The application has been preconfigured to use the host-only IP http://22.22.22.10 and forwards the VM port ``80`` to ``8000`` so http://localhost:8000 is available as well.

Adding a host alias is recommended. This can be done by adding the following line to  ``/etc/hosts``::

    22.22.22.10    local-us-ignite.org

Once this is done the application will be available at http://local-us-ignite.org

The VM has been configured to run and reload the code changes automatically without user input.


Stopping the VM
---------------

The application can be stopped by running::

    vagrant halt


Starting the VM
-----------------

The aplication can be started by running::

    vagrant up


Updating the VM
---------------

From time to time the application will require new packages to be installed or new configuration. Once the changes have ben pulled via ``git`` the provisioner can be run with::

    vagrant provision

This will run any mechanics required to update the application.


Logging into the VM
-------------------

Interaction with the VM can be done via SSH, by running in the root of the repository::

    vagrant ssh


Access can be granted by using SSH directly, in order to do this an ssh config entry is required, the following command will add the required fields to ``~/.ssh/config``::

    vagrant ssh-config --host us_ignite | sed -e '$a\' | tee -a ~/.ssh/config

Once this has been done the VM is accessible via::

    ssh us_ignite


Running it in Heroku
--------------------

The application has already been bootstrapped to run in Heroku and it is available at: http://us-ignite.herokuapp.com/


Configuring the development environment
---------------------------------------

The deployment to Heroku is done using ``git`` as a transport.

Any interaction with the repository is done via ``fabric``, All the fabric commands require that the Heroku ``git`` repository is aliased as ``production``. This can be done with::

    git remote add production git@heroku.com:us-ignite.git


.. note::

   In order to be able to contribute and deploy in the production application the developer needs to be added as a collaborator in Heroku.
