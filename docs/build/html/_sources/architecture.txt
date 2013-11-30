Architecture
============


Development application
-----------------------

The local application uses ``gunicorn`` and ``wsgi`` to reload automatically any changes in  the codebase without any developer interaction.

Whenever possible ``NGINX`` is used to serve any static assets, falling back to ``Django`` when the asset hasn't been found in the static directories.

In case as simple ``smtp`` server is required to test the email it can be activated by running **inside** the VM::

    $ run_smtp


Testing
-------

The tests are executed using python ``nose`` test runner, and they are located inside each django test application ``tests`` directory.

The test suite can be run from **inside** the VM with the following command::

  $ fab test

The test are unitary and do not access any network resource or remote storage system.

Front end
---------

Any reference to the static assets in the application must be prefixed by ``{{ STATIC_URL }}``. e.g.::

    {{ STATIC_URL }}images/background.jpg


Heroku
------

The application uses a combination of add-ons.

- An SMTP server is used to output emails.
- AWs S3 for storing any static assets, any static asset and user generated content is saved in S3.
- A key-storage system is used for caching applications.
- Python 2.7.4 runtime.
