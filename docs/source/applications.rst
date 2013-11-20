Applications
============

Applications are at the core of US Ignite

The applications were  modeled based on: https://etherpad.mozilla.org/ignite-site-app-entry

The applications can be at different stages:

 - Idea complete
 - Team complete / Forming team
 - Alpha version / developing alpha / testing alpha
 - Beta version / developing beta / in beta test
 - Demo-able / demoing
 - Deployable / deploying

Users have full control on the visibility of the application they can select between ``DRAFT`` and ``PUBLISHED``.

- ``Draft`` will make the application visible to the owner and members of the application.
- ``Published`` will make the application visible to everyone.

.. note::

    An special ``Removed`` status is provided for the admins to remove any inappropriate content, without deleting it.

The application can show the usage of the next gen characteristics.


Adding applications
-------------------

Applications can only be submited by registered users.


Application listing
-------------------

All the public ``Applications`` are listed in the listing view. They are paginated, and they can be ordered as well.


Application detail
------------------

The ``Application`` detail page is visible to everyone when published. When it is on ``Draft`` mode is only available for owners and members.

Github and Twitter URLS are automatically detected and if possible the profile page will show the latest 5 commits or tweets.


Application collaborators
-------------------------

The collaborators of an ``Application`` need to be registered. Only the owner of an application can add a collaborator.

A collaborator receives an extra set of permissions on a selected ``Application``.

The collaborators need to be added by ``email`` address, if the user is not registered the form will show an error.


Application versioning
----------------------

The owner of an application can generate a version of it for reference of what the application looked at a certain point.

The versioning functionality is available in the application profile page.

The visibility of the application is connected to the visibility ov the versions, this means that if the application is not visible the versions won't be visible either.
