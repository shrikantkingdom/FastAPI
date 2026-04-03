"""Teradata database connector."""
import logging
from typing import Any, List, Optional, Tuple

from app.db.connectors.base import BaseConnector

logger = logging.getLogger(__name__)


class TeradataConnector(BaseConnector):
    """
    Connects to Teradata using the *teradatasql* driver.
    Falls back to a mock when the driver is not installed (dev/test environments).
    """

    def _get_connection(self):
        try:
            import teradatasql  # type: ignore

            return teradatasql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database,
            )
        except ImportError:
            raise RuntimeError(
                "teradatasql is not installed. "
                "Install it with: pip install teradatasql"
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
            logger.warning(f"Teradata connection test failed: {exc}")
            return False
