from passlib.hash import sha512_crypt

from inbox.exception import UnauthorizedActionError
from inbox.model import Domain, Email, EmailStatus, RejectSender
from inbox.service.auth import active_account


def encrypt(string: str) -> str:
    return sha512_crypt.hash(string)


def list_emails() -> list[Email]:
    emails = (
        Email.select(
            Email.id,
            Email.username,
            Email.password,
            Email.domain,
            Email.forward_to,
            Email.status,
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
    status: EmailStatus,
    id: int | None = None,
    username: str | None = None,
    description: str | None = None,
) -> None:
    print("ABC")
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
        "status": status,
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


def list_reject_senders() -> list[RejectSender]:
    reject_senders = RejectSender.select(
        RejectSender.id,
        RejectSender.username,
        RejectSender.domain_name,
        RejectSender.description,
    ).order_by(RejectSender.domain_name, RejectSender.username)
    account = active_account()
    if not account:
        raise UnauthorizedActionError("No account is active")
    if not account.is_admin:
        reject_senders = reject_senders.where(
            RejectSender.account == active_account()
        )
    return list(reject_senders)


def upsert_reject_sender(
    username: str,
    domain_name: str,
    description: str | None = None,
    id: int | None = None,
) -> None:
    sender = RejectSender.get_or_none(RejectSender.id == id)
    kwargs = {
        "account": active_account(),
        "username": username,
        "domain_name": domain_name,
        "description": description,
    }
    if sender is None:
        sender = RejectSender.create(**kwargs)
    else:
        sender.update_from_dict(**kwargs)
        sender.save()


def delete_reject_sender(id: int) -> bool:
    sender = RejectSender.get_or_none(RejectSender.id == id)
    if sender is not None:
        if sender.account != active_account():
            raise UnauthorizedActionError(
                "Rejected sender does not belong to this account"
            )
        sender.delete_instance()
        return True
    return False
