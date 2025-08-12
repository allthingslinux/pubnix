from __future__ import annotations

from typing import Optional

from .base import AuthBackend


class LdapBackend(AuthBackend):
    def __init__(self, url: str, base_dn: str):
        self.url = url
        self.base_dn = base_dn

    def authenticate(self, username: str, password: str) -> bool:
        # TODO: implement LDAP bind
        return False

    def get_email(self, username: str) -> Optional[str]:
        return None
