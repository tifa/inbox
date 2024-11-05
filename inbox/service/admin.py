import crypt
import os

from inbox.exception import UnauthorizedActionError
from inbox.model import Domain, Email
from inbox.service.auth import active_account


def encrypt(string: str) -> str:
    salt = f"$6${os.urandom(16).hex()}"
    return crypt.crypt(string, salt)


def list_emails() -> list[Email]:
    emails = (
        Email.select(
            Email.id,
            Email.username,
            Email.password,
            Email.domain,
            Email.forward_to,
            Email.description,
        )
        .join(Domain)
        .order_by(Domain.name, Email.username)
    )
    account = active_account()
    if not account:
        raise UnauthorizedActionError("No account is active")
    if not account.is_admin:
        emails = emails.where(Domain.account == account)
    return list(emails)


def upsert_email(
    password: str,
    domain_id: int,
    forward_to: str,
    id: int | None = None,
    username: str | None = None,
    description: str | None = None,
) -> None:
    domain = Domain.get_or_none(Domain.id == domain_id)
    if domain.account != active_account():
        raise UnauthorizedActionError(
            "Domain for this email does not belong to this account"
        )
    email = Email.get_or_none(Email.id == id)
    kwargs = {
        "username": username,
        "password": encrypt(password),
        "domain": domain,
        "forward_to": forward_to,
        "description": description,
    }
    if email is None:
        email = Email.create(**kwargs)
    else:
        email.update_from_dict(**kwargs)
        email.save()


def delete_email(id: int) -> bool:
    email = Email.get_or_none(Email.id == id)
    if email is not None:
        if email.domain.account != active_account():
            raise UnauthorizedActionError(
                "Domain for this user does not belong this account"
            )
        email.delete_instance()
        return True
    return False


def list_domains() -> list[Domain]:
    domains = Domain.select(
        Domain.id, Domain.name, Domain.description
    ).order_by(Domain.name)
    account = active_account()
    if not account:
        raise UnauthorizedActionError("No account is active")
    if not account.is_admin:
        domains = domains.where(Domain.account == active_account())
    return list(domains)


def upsert_domain(
    name: str,
    description: str | None = None,
    id: int | None = None,
) -> None:
    domain = Domain.get_or_none(Domain.id == id)
    kwargs = {
        "account": active_account(),
        "name": name,
        "description": description,
    }
    if domain is None:
        domain = Domain.create(**kwargs)
    else:
        domain.update_from_dict(**kwargs)
        domain.save()


def delete_domain(id: int) -> bool:
    domain = Domain.get_or_none(Domain.id == id)
    if domain is not None:
        if domain.account != active_account():
            raise UnauthorizedActionError(
                "Domain does not belong to this account"
            )
        domain.delete_instance()
        return True
    return False