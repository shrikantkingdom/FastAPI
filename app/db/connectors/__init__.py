"""Database connector factory."""
from typing import Optional

from app.db.connectors.base import BaseConnector
from app.db.connectors.db2 import DB2Connector
from app.db.connectors.sqlserver import SQLServerConnector
from app.db.connectors.teradata import TeradataConnector

_REGISTRY = {
    "teradata": TeradataConnector,
    "db2": DB2Connector,
    "sqlserver": SQLServerConnector,
}


def get_connector(
    db_type: str,
    host: str,
    database: str,
    username: str,
    password: str,
    port: Optional[int] = None,
) -> BaseConnector:
    """Return the appropriate connector for *db_type*."""
    db_type = db_type.lower()
    cls = _REGISTRY.get(db_type)
    if cls is None:
        raise ValueError(
            f"Unsupported db_type '{db_type}'. Choose from: {list(_REGISTRY)}"
        )
    return cls(
        host=host,
        port=port,
        database=database,
        username=username,
        password=password,
    )
