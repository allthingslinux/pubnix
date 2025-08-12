"""Validation service for ATL Pubnix."""

import re
from typing import List


class ValidationService:
    """Service for validating user input and application data."""

    # Reserved usernames that cannot be used
    RESERVED_USERNAMES = {
        "root",
        "admin",
        "administrator",
        "www",
        "mail",
        "ftp",
        "ssh",
        "http",
        "https",
        "api",
        "app",
        "web",
        "server",
        "system",
        "daemon",
        "service",
        "user",
        "guest",
        "test",
        "demo",
        "example",
        "sample",
        "temp",
        "tmp",
        "bin",
        "sbin",
        "usr",
        "var",
        "etc",
        "opt",
        "home",
        "lib",
        "dev",
        "proc",
        "sys",
        "boot",
        "mnt",
        "media",
        "pubnix",
        "atl",
        "linux",
        "unix",
        "shell",
        "bash",
        "zsh",
        "fish",
        "csh",
    }

    def validate_username(self, username: str) -> bool:
        """Validate username format and availability."""
        if not username:
            return False

        # Check length
        if len(username) < 3 or len(username) > 32:
            return False

        # Check format (alphanumeric + underscore only)
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False

        # Must start with letter or underscore
        if not re.match(r"^[a-zA-Z_]", username):
            return False

        # Check against reserved usernames
        if username.lower() in self.RESERVED_USERNAMES:
            return False

        return True

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        if not email:
            return False

        # Basic email validation
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email))

    def validate_full_name(self, full_name: str) -> bool:
        """Validate full name."""
        if not full_name or len(full_name.strip()) < 1:
            return False

        if len(full_name) > 100:
            return False

        # Allow letters, spaces, hyphens, apostrophes, and periods
        name_pattern = r"^[a-zA-Z\s\-'.]+$"
        return bool(re.match(name_pattern, full_name.strip()))

    def get_username_requirements(self) -> List[str]:
        """Get list of username requirements."""
        return [
            "Must be 3-32 characters long",
            "Can only contain letters, numbers, and underscores",
            "Must start with a letter or underscore",
            "Cannot be a reserved system username",
        ]

    def get_validation_errors(
        self, username: str, email: str, full_name: str
    ) -> List[str]:
        """Get list of validation errors for application data."""
        errors = []

        if not self.validate_username(username):
            errors.append("Invalid username format")

        if not self.validate_email(email):
            errors.append("Invalid email format")

        if not self.validate_full_name(full_name):
            errors.append("Invalid full name")

        return errors
