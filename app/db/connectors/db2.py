"""IBM DB2 database connector."""
import logging
from typing import Any, List, Optional, Tuple

from app.db.connectors.base import BaseConnector

logger = logging.getLogger(__name__)


class DB2Connector(BaseConnector):
    """
    Connects to IBM DB2 using the *ibm_db* driver.
    Falls back gracefully when the driver is absent.
    """

    DEFAULT_PORT = 50000

    def _get_connection(self):
        try:
            import ibm_db  # type: ignore
            import ibm_db_dbi  # type: ignore

            port = self.port or self.DEFAULT_PORT
            conn_str = (
                f"DATABASE={self.database};"
                f"HOSTNAME={self.host};"
                f"PORT={port};"
                f"PROTOCOL=TCPIP;"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
            ibm_conn = ibm_db.connect(conn_str, "", "")
            return ibm_db_dbi.Connection(ibm_conn)
        except ImportError:
            raise RuntimeError(
                "ibm_db is not installed. Install it with: pip install ibm_db"
            )

    def execute(
        self, query: str, params: Optional[List[Any]] = None
    ) -> Tuple[List[str], List[List[Any]]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        columns = [desc[0] for desc in cursor.description or []]
        rows = [list(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return columns, rows

    def test_connection(self) -> bool:
        try:
            conn = self._get_connection()
            conn.close()
            return True
        except Exception as exc:
            logger.warning(f"DB2 connection test failed: {exc}")
            return False
