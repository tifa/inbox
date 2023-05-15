Managing Aliases
================

At the moment aliases are managed through direct sqlite querying, so here's a
cheatsheet.

Add Domains
-----------

.. prompt::

    INSERT INTO domains (domain_name) VALUES ('example.com');

Add Emails
----------

To create a catch-all, replace the username with ``NULL``.

.. prompt::

    INSERT INTO users (username, domain_id, password, forward_to, description)
    SELECT 'user1', domain_id, md5('password1'), 'forward@email.net', 'My email'
    FROM domains
    WHERE domain_name = 'example.com';
