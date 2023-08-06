Email Restrictions
==================

At the moment sender/recipient policies are managed through direct sqlite
querying, so here's a cheatsheet.

Reject Senders
--------------

Reject incoming mail from specific email addresses with a ``REJECT`` response.

.. prompt::

    INSERT INTO reject_senders (username, domain_name, description)
    VALUES ('user1', 'example.org', 'Spamming me');

Reject Recipients
-----------------
Reject incoming mail to specific email addresses with a ``REJECT`` response.
These take precedence over any catch-alls in the ``users`` table.

.. prompt::

    INSERT INTO reject_recipients (username, domain_id, memo)
    SELECT 'user1', domain_id, 'Company had a data leak'
    FROM `domains`
    WHERE domain_name = 'example.com';
