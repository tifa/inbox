import re
from datetime import datetime

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    Proxy,
    TextField,
)

from inbox.exception import ValidationError

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


db_proxy = Proxy()


class BaseModel(Model):
    time_created = DateTimeField(default=datetime.now)
    time_updated = DateTimeField(null=True)

    class Meta:
        database = db_proxy

    def validate(self) -> None:
        pass

    def save(self, *args, **kwargs) -> bool:
        self.validate()
        if self.get_id() is not None:
            self.time_updated = datetime.now()  # type: ignore
        return super().save(*args, **kwargs)

    def update_from_dict(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _validate_email(self, email: str) -> None:
        if email and not re.match(EMAIL_REGEX, email):
            raise ValidationError(f"Invalid email address: {email}")


class Account(BaseModel):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=255)
    is_admin = BooleanField(default=False)


class Domain(BaseModel):
    account = ForeignKeyField(Account, backref="domain")
    name = CharField(max_length=50)
    description = TextField(null=True)

    class Meta:
        indexes = ((("account", "name"), True),)

    @property
    def emails(self) -> list["Email"]:
        return list(Email.select().where(Email.domain == self))


class Email(BaseModel):
    username = CharField(max_length=50, null=True)
    domain = ForeignKeyField(Domain, backref="email")
    password = CharField(max_length=255)
    forward_to = CharField(max_length=255)
    description = TextField(null=True)

    class Meta:
        indexes = ((("username", "domain"), True),)

    def validate(self) -> None:
        self._validate_email(self.forward_to)


class RejectRecipient(BaseModel):
    username = CharField(max_length=50)
    domain = ForeignKeyField(Domain, backref="reject_recipient")
    description = TextField(null=True)

    class Meta:
        indexes = ((("username", "domain"), True),)
        table_name = "reject_recipient"


class RejectSender(BaseModel):
    account = ForeignKeyField(Account, backref="reject_sender")
    username = CharField(max_length=50, null=True)
    domain_name = CharField(max_length=50)
    description = TextField(null=True)

    class Meta:
        indexes = ((("account", "username", "domain_name"), True),)
        table_name = "reject_sender"
