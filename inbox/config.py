import os

sqlite_db = os.environ.get("SQLITE_DB")
if sqlite_db == "file":
    SQLITE_DB_PATH = "/data/db.sqlite"
elif sqlite_db == "memory":
    SQLITE_DB_PATH = ":memory:"
else:
    raise ValueError(f"Invalid value for SQLITE_DB: {sqlite_db}")
