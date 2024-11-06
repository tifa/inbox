from unittest.mock import patch

import pytest

from inbox.exception import UnauthorizedActionError
from inbox.model import Domain, Email
from inbox.service.admin import (
    delete_domain,
    delete_email,
    list_domains,
    list_emails,
    upsert_domain,
    upsert_email,
)


def test_list_emails(account):
    domain = Domain.create(account=account, name="example.org")
    email = Email.create(
        password="password",
        domain=domain,
        forward_to="email@example.com",
    )

    with patch("inbox.service.admin.active_account", return_value=account):
        assert list_emails() == [email]


@pytest.mark.parametrize("account", [2], indirect=["account"])
def test_list_emails_accounts(account, admin):
    account_1, account_2 = account

    domain_1 = Domain.create(account=account_1, name="example.org")
    domain_2 = Domain.create(account=account_2, name="example.net")
    domain_3 = Domain.create(account=account_1, name="example.com")
    domain_4 = Domain.create(account=admin, name="example.co")

    email_1 = Email.create(
        password="password1",
        domain=domain_1,
        forward_to="email@example.co",
    )
    email_2 = Email.create(
        password="password2",
        domain=domain_2,
        forward_to="email@example.com",
    )
    email_3 = Email.create(
        password="password3",
        domain=domain_3,
        forward_to="email@example.net",
    )
    email_4 = Email.create(
        password="password4", domain=domain_4, forward_to="email@example.org"
    )

    with patch("inbox.service.admin.active_account", return_value=account_1):
        assert list_emails() == [email_3, email_1]
    with patch("inbox.service.admin.active_account", return_value=account_2):
        assert list_emails() == [email_2]
    with patch("inbox.service.admin.active_account", return_value=admin):
        assert list_emails() == [email_4, email_3, email_2, email_1]


def test_upsert_email(account):
    domain = Domain.create(account=account, name="example.org")

    emails_args = [
        {
            "username": "username1",
            "password": "password1",
            "forward_to": "email1@example.com",
            "description": "description1",
        },
        {
            "username": "username2",
            "password": "password2",
            "forward_to": "email2@example.com",
            "description": "description2",
        },
        {
            "id": 1,
            "username": "username3",
            "password": "password1",
            "forward_to": "email1@example.com",
            "description": "description1",
        },
    ]

    for i, email_arg in enumerate(emails_args, start=1):
        with patch("inbox.service.admin.active_account", return_value=account):
            upsert_email(domain_id=domain.id, **email_arg)
        email = Email.get(Email.id == email_arg.get("id", i))
        assert email.username == email_arg["username"]
        # assert email.password == email_arg["password"]
        # TODO: Fix password encryption
        assert email.domain == domain
        assert email.forward_to == email_arg["forward_to"]
        assert email.description == email_arg["description"]


@pytest.mark.parametrize("account", [2], indirect=["account"])
def test_upsert_email_account(account):
    account_1, account_2 = account
    domain_1 = Domain.create(account=account_1, name="example.com")

    with (
        patch("inbox.service.admin.active_account", return_value=account_2),
        pytest.raises(UnauthorizedActionError),
    ):
        upsert_email(
            password="password",
            domain_id=domain_1.id,
            forward_to="hello@example.net",
        )


def test_delete_email(account):
    assert not delete_email(id=1)

    domain = Domain.create(account=account, name="example.org")
    Email.create(
        password="password",
        domain=domain,
        forward_to="email@example.com",
    )
    with patch("inbox.service.admin.active_account", return_value=account):
        assert delete_email(id=1)

    assert Email.get_or_none(Email.id == 1) is None


@pytest.mark.parametrize("account", [2], indirect=["account"])
def test_delete_email_accounts(account):
    account_1, account_2 = account
    domain_1 = Domain.create(account=account_1, name="example.com")
    Email.create(
        password="password", domain=domain_1, forward_to="email@example.net"
    )

    with (
        patch("inbox.service.admin.active_account", return_value=account_2),
        pytest.raises(UnauthorizedActionError),
    ):
        delete_email(id=1)


def test_list_domains(account):
    domain_1 = Domain.create(account=account, name="example.net")
    domain_2 = Domain.create(account=account, name="example.com")

    email = Email.create(
        password="password", domain=domain_2, forward_to="email@example.com"
    )

    with patch("inbox.service.admin.active_account", return_value=account):
        assert list_domains() == [domain_2, domain_1]

    assert domain_1.emails == []
    assert domain_2.emails == [email]


@pytest.mark.parametrize("account", [2], indirect=["account"])
def test_list_domains_accounts(account, admin):
    account_1, account_2 = account

    domain_1 = Domain.create(account=account_1, name="example.com")
    domain_2 = Domain.create(account=account_2, name="example.net")
    domain_3 = Domain.create(account=account_1, name="example.org")
    domain_4 = Domain.create(account=admin, name="example.co")

    with patch("inbox.service.admin.active_account", return_value=account_1):
        assert list_domains() == [domain_1, domain_3]
    with patch("inbox.service.admin.active_account", return_value=account_2):
        assert list_domains() == [domain_2]
    with patch("inbox.service.admin.active_account", return_value=admin):
        assert list_domains() == [domain_4, domain_1, domain_2, domain_3]


def test_upsert_domain(account):
    domains_args = [
        {
            "name": "example.com",
            "description": "description1",
        },
        {
            "name": "example.net",
            "description": "description2",
        },
        {
            "id": 1,
            "name": "example.org",
            "description": "description1",
        },
    ]

    for i, domain_arg in enumerate(domains_args, start=1):
        with patch("inbox.service.admin.active_account", return_value=account):
            upsert_domain(**domain_arg)
        domain = Domain.get(Domain.id == domain_arg.get("id", i))
        assert domain.name == domain_arg["name"]
        assert domain.description == domain_arg["description"]
        assert domain.account == account


def test_delete_domain(account):
    assert not delete_domain(id=1)

    Domain.create(account=account, name="example.com")

    with patch("inbox.service.admin.active_account", return_value=account):
        assert delete_domain(id=1)

    assert Domain.get_or_none(Domain.id == 1) is None


# @pytest.mark.parametrize("account", [2], indirect=["account"])
# def test_delete_domain_account(account):
#     account_1, account_2 = account
#     domain_1 = Domain.create(account=account_1, name="example.com")

#     with (
#         patch("inbox.service.admin.active_account", return_value=account_2),
#         pytest.raises(UnauthorizedActionError),
#     ):
#         delete_domain(id=1)
