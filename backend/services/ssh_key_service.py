"""SSH key parsing and validation utilities."""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from typing import List

ALLOWED_ALGORITHMS = {
    "ssh-ed25519",
    "ssh-rsa",
    "ecdsa-sha2-nistp256",
    "ecdsa-sha2-nistp384",
    "ecdsa-sha2-nistp521",
}


@dataclass
class ParsedKey:
    algorithm: str
    key_b64: str
    comment: str
    fingerprint: str  # SHA256 base64 without trailing '='


class SshKeyService:
    @staticmethod
    def parse_public_key(public_key: str) -> ParsedKey:
        parts = public_key.strip().split()
        if len(parts) < 2:
            raise ValueError("Invalid public key format")
        algorithm, key_b64 = parts[0], parts[1]
        comment = parts[2] if len(parts) >= 3 else ""

        if algorithm not in ALLOWED_ALGORITHMS:
            raise ValueError("Unsupported key algorithm")

        try:
            key_bytes = base64.b64decode(key_b64.encode("ascii"), validate=True)
        except Exception as exc:
            raise ValueError("Invalid base64 in public key") from exc

        fp_raw = hashlib.sha256(key_bytes).digest()
        fp_b64 = base64.b64encode(fp_raw).decode("ascii").rstrip("=")

        return ParsedKey(
            algorithm=algorithm, key_b64=key_b64, comment=comment, fingerprint=fp_b64
        )

    @staticmethod
    def build_authorized_keys(keys: List[str]) -> str:
        """Build authorized_keys content from a list of public keys."""
        valid_lines: list[str] = []
        for key in keys:
            parsed = SshKeyService.parse_public_key(key)
            valid_lines.append(
                f"{parsed.algorithm} {parsed.key_b64} {parsed.comment}".strip()
            )
        return "\n".join(valid_lines) + ("\n" if valid_lines else "")
