Development Guide
=================

Dev Environment
---------------

The main differene in the development environment is that it allows you to
bring up an empty server with dependencies installed and the source code mounted
as a volume.

.. prompt:: bash $

    make dev

Once you're in, provision the server.

.. prompt:: bash dev~$

    make

Or run it in two parts like this:

.. prompt:: bash dev~$

    make base
    make update

In prod, changes from ``make base`` are pre-installed in the image whereas
changes from ``make update`` (``.env``-affected configurations) are applied at
runtime.


Useful Resources
----------------

`All About SPAM <http://allaboutspam.com>`_
    An online email server test to check basic security settings


Schema
------

.. graphviz:: _static/graphviz/database.dot
