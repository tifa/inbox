virtualmail
===========

A mail server that forwards and sends emails through virtual aliases.

- Create catch-alls (``*@example.com``).
- Block emails from unwanted senders or incoming emails to compromised aliases
  with custom SMTP error messages.
- Send emails using an alias.
- Generate daily report summaries of mail transfer activity.

Documentation
-------------

:doc:`getting-started`
   How to install and get the server up and running

:doc:`managing-aliases`
   Manage email aliases

:doc:`email-restrictions`
   Restrict incoming emails

:doc:`sending-emails`
   Sending emails using an alias


Development
-----------

:doc:`development-guide`
   Bring up a development environment

:doc:`todo-list`
   List of things to implement


.. toctree::
   :maxdepth: 2
   :caption: Documentation
   :hidden:

   getting-started
   managing-aliases
   email-restrictions
   sending-emails

.. toctree::
   :maxdepth: 2
   :caption: Development
   :hidden:

   development-guide
   todo-list
