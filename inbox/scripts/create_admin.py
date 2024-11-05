#!/usr/bin/python3

import click
from argon2 import PasswordHasher

from inbox.database import initialize_db
from inbox.model import Account


@click.command()
@click.option("--username", prompt=True, help="The username for the new admin")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password for the new admin",
)
def create_admin(username: str, password: str) -> None:
    initialize_db()

    try:
        Account.create(
            username=username,
            password=PasswordHasher().hash(password),
            is_admin=True,
        )
        click.echo(f"Admin '{username}' created successfully")
    except Exception as e:
        click.echo(f"Error creating account: {e}")


if __name__ == "__main__":
    create_admin()
