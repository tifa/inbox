# inbox 💌

A mail server that forwards and sends emails through virtual aliases.

- Create catch-alls (`*@example.com`)
- Multiple domains
- Block emails from unwanted senders
- Block incoming emails to compromised aliases
- Generate daily report summaries of mail transfer activity
- Powered by [Postfix] and [Dovecot]

## Usage

### Domains

```
domain add example.com    Add a domain
domain rm example.com     Remove a domain
domain rm -f example.com  Remove a domain and all emails associated with it
domain ls                 List all domains
```

### Emails

```
email add user@example.com other@email.com    Add a forwarder
email add *@example.com other@email.com       Add a catch-all forwarder
email rm user@example.com                     Remove a forwarder
email rm *@example.com                        Remove a catch-all or all emails in this domain
email ls                                      List all emails
email ls example.com                          List all emails from this domain
```

### Filters

```
deny from add bad@actor.com           Blacklist emails from this sender
deny from rm bad@actor.com            Remove this sender from the blacklist
deny from ls                          List all blacklisted senders
deny to add compromised@example.com   Block incoming emails to this recipient
deny to rm compromised@example.com    Remove the block for this recipient
deny to ls                            List all recipients blocked from receiving emails
```

## Setup

### Requirements

- Ansible
- RHEL or CentOS instance
- Open outgoing port 25

### SSH key pair

Create a key pair.

```sh
ssh-keygen -t ed25519 -f ~/.ssh/mail
```

### Configuration

Copy this template to configure the `config` file.

```sh
cp config.example config
```

### Bootstrap

Run the interactive bootstrap Ansible playbook on a brand new instance, which will:

- Create a new sudoer
- Change the SSH port
- Install the public key, if one does not already exist
- Change the existing user ("root") password and disable logins for root
- Disable password-based authentication in favor of public-key authentication

```sh
SSH_PUB_KEY=~/.ssh/mail.pub \
  make bootstrap
```

Where `SSH_PUB_KEY` is the path to the public SSH key to install for the new admin.

If the instance comes pre-installed with a key, pass in the `ROOT_SSH_PRIV_KEY` or the path to the private key for root.

```sh
SSH_PUB_KEY=~/.ssh/mail.pub \
ROOT_SSH_PRIV_KEY=~/.ssh/root \
  make bootstrap
```

### Provision

Provision the mail server.

```sh
make provision
```


## Contributing

### Requirements

- Docker



<!-- Links -->
[Dovecot]: https://dovecot.org
[Postfix]: https://postfix.org
