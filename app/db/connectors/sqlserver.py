"""SQL Server database connector."""
import logging
from typing import Any, List, Optional, Tuple

from app.db.connectors.base import BaseConnector

logger = logging.getLogger(__name__)


class SQLServerConnector(BaseConnector):
    """
    Connects to Microsoft SQL Server using the *pyodbc* driver.
    Falls back gracefully when the driver is absent.
    """

    DEFAULT_PORT = 1433

    def _get_connection(self):
        try:
            import pyodbc  # type: ignore

            port = self.port or self.DEFAULT_PORT
            conn_str = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                f"SERVER={self.host},{port};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
            return pyodbc.connect(conn_str)
        except ImportError:
            raise RuntimeError(
                "pyodbc is not installed. Install it with: pip install pyodbc"
            )

    def execute(
        self, query: str, params: Optional[List[Any]] = None
    ) -> Tuple[List[str], List[List[Any]]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            columns = [desc[0] for desc in cursor.description or []]
            rows = [list(row) for row in cursor.fetchall()]
            return columns, rows

    def test_connection(self) -> bool:
        try:
            conn = self._get_connection()
            conn.close()
            return True
        except Exception as exc:
            logger.warning(f"SQL Server connection test failed: {exc}")
            return False
