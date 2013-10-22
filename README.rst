.. 
Project for local-us-ignite.org
=============================

This project is capable to be run in Heroku and locally using Vagrant and one of its providers with puppet.


Running locally
---------------

In order to run the application locally you will require Vagrant and a provisioner installed in your local machine (VirtualBox being the easiest provisioner you can get hold of).

Once installed you can start the VM by runnning from the root of the repository, the following command::

  vagrant up

After the VM has been installed and provisioned the application should be available at http://22.22.22.10, a port forwarding from 80 to 8000 has been setup so you should be able to access http://localhost:8000 as well.

There are a few other commands that can help you to interact better with the VM.

Add the following line to ``/etc/hosts`` to access the VM via http://local-us-ignite.org ::

    22.22.22.10    local-us-ignite.org


Add an ssh config entry for this project, so you can access the VM with ``ssh us_ignite::

    vagrant ssh-config --host us_ignite | sed -e '$a\' | tee -a ~/.ssh/config


Running it in heroku
--------------------

The application has been bootstrapped to heroku and it is available in the following URL http://us-ignite.herokuapp.com/

In order for the fabric scripts to work the heroku application needs to be added with the ``production`` alias::

    $ git remote add production git@heroku.com:us-ignite.git

Please note that you will only be able to deploy if you have been added as a collaborator for the project.
