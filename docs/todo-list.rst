TODO List
=========

In Progress
-----------
- Migrate docs to `Sphinx <https://www.sphinx-doc.org/en/master/>`_.

Pending
-------
- Revisit all `Postfix <http://www.postfix.org/documentation.html>`_ and
  `Dovecot <https://doc.dovecot.org/configuration_manual/howto/postfix_dovecot_lmtp/>`_.
  configs. Aside from a few policy changes most of these haven't really been
  touched since I first set this up years ago.
- Option to directly install on the host machine instead of Docker.
- Fix mail sending from the local environment.
- Replace password MD5 hashing with something more secure.
- A lightweight web framework (e.g. `Bottle <https://bottlepy.org/docs/dev/index.html>`_,
  `Flask <https://flask.palletsprojects.com/>`_) to manage aliases instead of
  direct sqlite query inputs.
- Tests.
- Persist SSL certificates outside of the container. There is a limit to how
  many times we can generate/renew a certificate before we get `locked out
  <https://letsencrypt.org/docs/rate-limits/>`_ of Let's Encrypt for a week.
  This becomes a problem during testing. Might designate a folder on the host
  machine to store these along with the database.
- Track config file hash to determine if an update is needed.
- Add `BATV <https://en.wikipedia.org/wiki/Bounce_Address_Tag_Validation>`_ checking.
- Make fail2ban configurable.
- Check that the DNS DKIM record is configured during setup.

Complete
--------
- Migrate from CentOS to Ubuntu.
- Replace MySQL/phpMyAdmin with `sqlite3 <https://www.postfix.org/SQLITE_README.html>`_.

