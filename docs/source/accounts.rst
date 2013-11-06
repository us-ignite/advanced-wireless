Accounts
========

The accounts are created by using two systems, each having a different flow:

- Mozilla Persona.
- US Ignite registration.

The ``email`` is used as the username in the application.

Mozilla Persona
---------------

If the user has an existing Mozilla Persona account or generates one, the flow is as follows:

- User click the Mozilla Persona button.
- Server side validation and account creation.
- User receives welcome email.
- User is authenticated and ready to start using the application.


US Ignite registration
----------------------

Regular registration is offered in the website in case the user prefer so, the journey is as follow:

- User introduces email and password.
- User receives an email with a unique activation code, valid for a few days.
- User activates the account.
- User receives welcome email.
- User is able to authenticate with the credentials provided.


Invite users
------------

A section in the admin has been provided to invite users in batches. Each user should be listed in a new line and the format must be as follows::

    FULL_NAME, EMAIL_ADDRESS

The application will validate each record being imported, if a record do not comply with the following format, data corruption is assumed and import won't be performed.

After the records have been imported the application will create new accounts for each user and send an invitation email.

Please note that if an email has already been imported or has an existing account it will be ignored.

The journey is as follow:

- User gives US Ignite details and accepts to be subscribed.
- US Ignite imports the users.
- User receives invitation email.
- User clicks on unique URL and must login via Mozilla Persona.
