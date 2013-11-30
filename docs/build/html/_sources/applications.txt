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

Adding applications
-------------------

Applications can only be added by registered users. The information that can be added and listed as part of the application profile is:

- Name
- Summary
- Description
- Images that support the app.
- Links that support the app.
- List of NextGen features that it uses.
- Main domain of application of this app.


Application listing
-------------------

All the public ``Applications`` are listed in the listing view. The listing includes

- Pagination.
- Ordering.

Application detail
------------------

The ``Application`` detail page is visible to everyone when published. When it is on ``Draft`` mode is only available for owners and members.

Github and Twitter URLS are automatically detected and if possible the profile page will show the latest 5 commits or tweets.

.. note::
    The applications owned by a user will be listed in the user profile.


Application edit
----------------

The ``Application`` can only be edited by the ``owner`` of the application.

Application collaborators
-------------------------

The collaborators of an ``Application`` need  to be registered since being a member of an application gives the account extra permissions for the application. Only the owner of an application can add a collaborator.

A collaborator receives an extra set of permissions on a selected ``Application``.

The collaborators need to be added by ``email`` address, if the user is not registered the form will show an error.


Application community membershiop
---------------------------------

The application can be part of several communities, a link in the application profile page is provided to modify this.


Application versioning
----------------------

The owner of an application can generate a version of it for reference of what the application looked at a certain point.

The versioning functionality is available in the application profile page.

The visibility of the application is connected to the visibility ov the versions, this means that if the application is not visible the versions won't be visible either.

Backing up applications
-----------------------

Collaborators and owners of an application can backup the details of the applications by creating an export of the existing status of the application.


Awards
------

The applications can be awareded to show progress or recognize milestones.


Featured applications
---------------------

The applications can be listed in a featured curated ``Page`` these applications can be ordered.

When a ``Page`` is feature it uses the main slug for the featured applications. There can only be a single featured page, since it uses a special URL.

Older published pages can still be accessed using their canonical URLs.

