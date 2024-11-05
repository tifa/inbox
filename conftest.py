import pytest

from inbox.database import initialize_db
from inbox.model import Account


@pytest.fixture(autouse=True)
def db():
    initialize_db(force=True)
    yield


@pytest.fixture
def account(request):
    if hasattr(request, "param"):
        return [
            Account.create(username=f"username{i}", password=f"password{i}")
            for i in range(request.param)
        ]
    return Account.create(username="username", password="password")


@pytest.fixture
def admin():
    return Account.create(username="admin", password="password", is_admin=True)
