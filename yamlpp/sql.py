"""
Foundation of the SQLAlchemy binding

Not a lot of code, but carefully crafted.
"""

from typing import Any

# This module exports sql_create_engine and SQLConnection
from sqlalchemy import create_engine as sql_create_engine, text as sql_text
from sqlalchemy.engine import Connection as SQLConnection
from sqlalchemy.exc import OperationalError as SQLOperationalError



ElementaryTable = list[dict[str, Any]]

def sql_query(engine, query) -> ElementaryTable:
    "Make a query on an engine"
    with engine.begin() as conn:
        # we open with autocommit
        result = conn.execute(sql_text(query))
        if result.returns_rows:
            # it's important to map already at this stage
            # to immediately release the connection object.
            return result.mappings().all()
        else:
            return []
