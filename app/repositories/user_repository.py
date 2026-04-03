"""User repository – abstraction over the user store."""
from typing import Optional

from app.models.user import User


class UserRepository:
    """Simple in-memory user store. Swap for a real ORM repository in production."""

    _store: dict[str, User] = {}

    def get(self, username: str) -> Optional[User]:
        return self._store.get(username)

    def save(self, user: User) -> User:
        self._store[user.username] = user
        return user

    def delete(self, username: str) -> bool:
        if username in self._store:
            del self._store[username]
            return True
        return False
