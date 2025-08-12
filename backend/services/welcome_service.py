"""Dynamic welcome messages and system orientation."""

from __future__ import annotations

from datetime import datetime, timezone

from models import User


class WelcomeService:
    def build_welcome(self, user: User) -> dict[str, str]:
        return {
            "title": "Welcome to ATL Pubnix",
            "message": (
                f"Hello {user.full_name} (@{user.username})!\n"
                "Your home: ~/\n"
                "Web site: ~/public_html\n"
                "Use SSH keys for login; upload via the web/API.\n"
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
