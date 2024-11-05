from peewee import SqliteDatabase

from inbox.config import SQLITE_DB_PATH
from inbox.model import BaseModel, db_proxy
from inbox.util import get_all_subclasses

_DB = None


def initialize_db(force: bool = False) -> None:
    global _DB
    if _DB is None or force:
        _DB = SqliteDatabase(SQLITE_DB_PATH, pragmas={"foreign_keys": 1})

    _DB.connect()
    db_proxy.initialize(_DB)

    models = get_all_subclasses(BaseModel)
    _DB.create_tables(models)
