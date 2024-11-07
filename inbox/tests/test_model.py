import pytest
from peewee import IntegrityError

from inbox.exception import ValidationError
from inbox.model import Domain, Email, RejectSender


def test_domain(account):
    name = "example.com"
    description = "description"

    domain = Domain.create(account=account, name=name, description=description)
    assert domain.id == 1
    assert domain.name == name
    assert domain.description == description


def test_domain_missing():
    with pytest.raises(IntegrityError):
        Domain.create()


def test_domain_unique(account):
    name = "example.com"
    Domain.create(account=account, name=name)

    with pytest.raises(IntegrityError):
        Domain.create(account=account, name=name)


def test_email(account):
    domain = "example.com"

    username = "user"
    password = "pass"
    forward_to = "email@example.com"
    description = "description"

    domain = Domain.create(account=account, name="example.net")
    email = Email.create(
        username=username,
        password=password,
        domain=domain,
        forward_to=forward_to,
        description=description,
    )
    assert email.id == 1
    assert email.username == username
    assert email.password == password
    assert email.domain == domain
    assert email.forward_to == forward_to
    assert email.description == description


@pytest.mark.parametrize(
    "missing_column",
    ["password", "domain", "forward_to"],
)
def test_email_missing(account, missing_column):
    domain = Domain.create(account=account, name="example.com")
    args = {
        "password": "password",
        "domain": domain,
        "forward_to": "email@example.com",
    }

    with pytest.raises(IntegrityError):
        del args[missing_column]
        Email.create(**args)


def test_email_invalid_forward_to():
    with pytest.raises(ValidationError):
        Email.create(
            password="pass",
            domain=1,
            forward_to="email",
        )


def test_email_unique(account):
    domain = Domain.create(account=account, name="example.com")
    args = {
        "username": "user",
        "password": "pass1",
        "domain": domain,
        "forward_to": "email@example.org",
    }
    Email.create(**args)

    args["password"] = "pass2"
    args["forward_to"] = "email@example.net"
    with pytest.raises(IntegrityError):
        Email.create(**args)


def test_reject_sender(account):
    username = "user"
    domain_name = "example.com"
    description = "description"

    reject_sender = RejectSender.create(
        account=account,
        username=username,
        domain_name=domain_name,
        description=description,
    )
    assert reject_sender.id == 1
    assert reject_sender.username == username
    assert reject_sender.domain_name == domain_name
    assert reject_sender.description == description


def test_reject_sender_missing():
    with pytest.raises(IntegrityError):
        RejectSender.create()
