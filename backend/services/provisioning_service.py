"""User account provisioning service for ATL Pubnix.

This service encapsulates the logic to create system-level user accounts,
prepare their home directories, and deploy initial skeleton files.

In development and tests, it operates in dry-run mode and never executes
system commands. In production, it can be configured to execute commands
via a pluggable runner.
"""

from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

from models import User


@dataclass
class ProvisionResult:
    success: bool
    commands: List[str]
    message: str = ""


ShellRunner = Callable[[List[str]], int]


class ProvisioningService:
    """Service to provision system users and setup home directories."""

    def __init__(
        self,
        shell_runner: Optional[ShellRunner] = None,
        env: Optional[str] = None,
        skeleton_dir: Optional[str] = None,
        default_shell: str = "/bin/bash",
    ) -> None:
        self.env = (env or os.getenv("PUBNIX_ENV", "development")).lower()
        self.shell_runner = shell_runner or self._default_runner
        self.skeleton_dir = skeleton_dir or os.getenv(
            "PUBNIX_SKEL_DIR", str(Path(__file__).resolve().parent.parent / "skel")
        )
        self.default_shell = default_shell

    def _default_runner(self, argv: List[str]) -> int:
        completed = subprocess.run(argv, check=False)
        return completed.returncode

    def build_commands(self, user: User) -> List[str]:
        """Build the list of system commands required to provision the user."""
        username = user.username
        home = user.home_directory or f"/home/{username}"
        skel = self.skeleton_dir
        shell = user.shell or self.default_shell

        # useradd with home creation and skeleton
        commands = [
            f"useradd -m -d {shlex.quote(home)} -s {shlex.quote(shell)} -k {shlex.quote(skel)} {shlex.quote(username)}",
            # Ensure public_html exists
            f"mkdir -p {shlex.quote(home)}/public_html",
            f"chown -R {shlex.quote(username)}:{shlex.quote(username)} {shlex.quote(home)}/public_html",
            # Reasonable default permissions
            f"chmod 755 {shlex.quote(home)}",
            f"chmod 755 {shlex.quote(home)}/public_html",
        ]
        return commands

    def provision_user(
        self, user: User, dry_run: Optional[bool] = None
    ) -> ProvisionResult:
        """Provision the given user account on the host system.

        In non-production environments, defaults to dry-run (no command execution).
        """
        is_dry_run = dry_run if dry_run is not None else (self.env != "production")
        commands = self.build_commands(user)

        if is_dry_run:
            return ProvisionResult(
                success=True,
                commands=commands,
                message="Dry run: commands not executed",
            )

        # Execute commands sequentially; stop on first failure
        for cmd in commands:
            argv = [c for c in shlex.split(cmd) if c]
            rc = self.shell_runner(argv)
            if rc != 0:
                return ProvisionResult(
                    success=False,
                    commands=commands,
                    message=f"Command failed with code {rc}: {cmd}",
                )

        return ProvisionResult(success=True, commands=commands, message="Provisioned")
