"""Abstract base class for database connectors."""
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple


class BaseConnector(ABC):
    def __init__(
        self,
        host: str,
        database: str,
        username: str,
        password: str,
        port: Optional[int] = None,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    @abstractmethod
    def execute(
        self,
        query: str,
        params: Optional[List[Any]] = None,
    ) -> Tuple[List[str], List[List[Any]]]:
        """Execute *query* and return (column_names, rows)."""

    @abstractmethod
    def test_connection(self) -> bool:
        """Return True if connection succeeds, False otherwise."""
