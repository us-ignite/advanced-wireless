US Ignite website
-----------------

US Ignite fosters the creation of next-generation Internet applications that provide transformative public benefit.

By engaging diverse public and private leaders, we “ignite” the development and deployment of new apps with profound impact on how Americans work, live, learn and play.

Runnining the development server
--------------------------------

Vagrant is recommended installation path, since all the dependencies are installed inside the VM, and is closer to the deployment environment.


Requisites
----------

The following packages must be installed locally before the VM can be started.

- VirtualBox: https://www.virtualbox.org/wiki/Downloads
- Vagrant: https://www.vagrantup.com/downloads.html


After these packages have been installed, a plugin is required to make sure that the VM has always the latest help packages. This can be installed with::

    vagrant plugin install vagrant-vbguest


Running the VM
--------------

Once the pre-requisites have been installed the application can be started with the following command::

  vagrant up

.. note::

   The provisioning will take a while, since it needs to get a copy of the OS box and install any packages required.

The application has been preconfigured to use the host-only IP http://22.22.22.10 and forwards the VM port ``80`` to ``8000`` so http://localhost:8000 is available as well.

Adding a host alias is recommended. This can be done by adding the following line to  ``/etc/hosts``::

    22.22.22.10    local-us-ignite.org

Once this is done the application will be available at http://local-us-ignite.org

The VM has been configured to run and reload the code changes automatically without user input. But in case the application server needs to be reloaded it can be done from inside the VM with the following command::

    sudo service us_ignite restart

