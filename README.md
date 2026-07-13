# inbox 💌

A mail server that forwards and sends emails through virtual aliases.

- Create catch-alls (`*@example.com`)
- Multiple domains
- Block emails from unwanted senders
- Block incoming emails to compromised aliases
- Powered by [Postfix], [Dovecot], [SQLite], [NiceGUI], [Peewee], [Docker]

## Setup

### Requirements

- Ubuntu instance
- Open outgoing port 25
- Reverse DNS
- Python 3.10+

Set up the new instance using [server] and create a reverse proxy and set up
certificates using [service].


## Configuration

Copy the `.env` template and configure the application.

```sh
cp .env.template .env
```


## Provision

Provision the mail server to install and configure Postfix, Dovecot, OpenDKIM,
and fail2ban.

```sh
make provision
```

## Admin UI

Bring up the admin UI.

```sh
make ui
```

<!-- Links -->
[Docker]: https://docker.com
[Dovecot]: https://dovecot.org
[NiceGUI]: https://nicegui.io
[Peewee]: https://github.com/coleifer/peewee
[Postfix]: https://postfix.org
[SQLite]: https:/sqlite.org

[server]: https://github.com/tifa/server
[service]: https://github.com/tifa/service
