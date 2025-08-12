"""Authentication backend interfaces for future integrations (LDAP/SSO)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class AuthBackend(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> bool:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def get_email(self, username: str) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError
