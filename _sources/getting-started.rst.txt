Getting Started
===============

How to install and get the server up and running.


Steps
-----

At the domain registrar, create an A record to point to the IP address of the
mail server under ``example.com``.

.. list-table::
    :header-rows: 1

    * - Type
      - Name
      - Value
    * - A
      - mail
      - ``<IP ADDRESS>``

On the host machine, allow ports 25, 587, and 80 to pass through the firewall.

.. prompt:: bash $

    ufw allow 25/tcp
    ufw allow 587/tcp
    ufw allow Apache
    ufw -f enable

Clone this repository.

.. prompt:: bash $

    git clone https://github.com/tifa/virtualmail.git
    cd virtualmail

Copy ``example.env`` to ``.env`` and update the configuration.

.. prompt:: bash $

    cp example.env .env
    vi .env

.. config:option:: ADMIN_EMAIL

    :type: string
    :example: admin@example.net

    The email address of the administrator. Logged reports will be sent to this
    address. Preferably this is not an email address that is hosted on this
    server.

.. config:option:: MAILHOST

   :type: string
   :example: mail.example.com

   Hostname of the mail server.

.. config:option:: SQLITE_DB_PATH

   :type: string
   :example: /home/virtualmail/app.db

   Path to the sqlite3 database file that will contain all of the alias
   credentials. This file lives on the host machine and is mounted to the
   Docker container at ``/virtualmail/data/app.db``, which means the database
   will be intact even if the mail server is restarted. If one doesn't exist, it
   will be created during setup. Secure this file in a safe place, limit access,
   and back up often.

Build and start the service.

.. prompt:: bash $

    make build
    make start

.. admonition:: See also

    For a full list of available commands, run ``make help``.

Start adding aliases using ``sqlite3 /virtualmail/data/app.db`` in
``make shell`` and run this interactive setup process for each domain added:

.. prompt:: bash $

    HOSTNAME=example.net make domain

This will ask you to add several TXT records for DKIM and SPF, if you haven't
already. For DKIM, you'll see something like this:

.. prompt:: bash $

    TASK [mail : add TXT record for example.net] *******************************
    [mail : add TXT record for example.net]
    YYYY-MM-DD._domainkey	IN	TXT	( "v=DKIM1; h=sha256; k=rsa; "
        "p=<long-string-1>"
        "<long-string-2>" )  ; ----- DKIM key YYYY-MM-DD for example.net:

Copy the entire string in ``TXT ( ... )``, but without the quotes so that it
looks something like this:

.. list-table::
    :header-rows: 1

    * - Type
      - Name
      - Value
    * - TXT
      - ``YYYY-MM-DD._domainkey``
      - ``v=DKIM1; h=sha256; k=rsa; p=<long-string-1><long-string-2>``

If you are using a subdomain, remember to append the prefix to the name
of the record e.g. ``YYYY-MM-DD._domainkey.sub.domain`` for
``sub.domain.example.net``.
