Sending Emails
==============

Send emails using an alias by authetnicating with the SMTP server.

Gmail
-----
To send an email as ``hello@example.net`` from your Gmail account through SMTP
server ``mail.example.com``.

#. Add a new entry for the alias for the in the ``users`` table.
#. Go to the `Accounts and Import <https://mail.google.com/mail/u/0/#settings/accounts>`_ settings
   page.
#. Under "Send mail as," click "Add another email address."

    .. image:: _static/img/gmail-send-mail-as.png

#. Enter the email alias and click "Next Step &gt;&gt;".

    .. image:: _static/img/gmail-add-alias.png

3. Enter the credentials.

    .. image:: _static/img/gmail-smtp-auth.png

#. An email will be sent to ``hello@example.net`` with a confirmation code.

    .. image:: _static/img/gmail-confirm-code.png

#. Done!

    .. image:: _static/img/gmail-result.png

