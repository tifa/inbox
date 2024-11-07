# inbox 💌

A mail server that forwards and sends emails through virtual aliases.

- Create catch-alls (`*@example.com`)
- Multiple domains
- Block emails from unwanted senders
- Block incoming emails to compromised aliases
- Generate daily report summaries of mail transfer activity
- Powered by [Postfix] and [Dovecot]

## Setup

### Requirements

- Ubuntu instance
- Open outgoing port 25
- Reverse DNS

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


<!-- Links -->
[Dovecot]: https://dovecot.org
[Postfix]: https://postfix.org

[server]: https://github.com/tifa/server
[service]: https://github.com/tifa/service
