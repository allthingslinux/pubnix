"""Backup and restore service for ATL Pubnix.

Creates compressed archives of important paths, encrypts them with Fernet
(AES-128-CBC + HMAC via cryptography's Fernet), writes a manifest with
checksums, and can verify and restore. Upload step is abstracted to a simple
filesystem copy to simulate remote storage (e.g., Hetzner Storage Box mount).
"""
from __future__ import annotations

import base64
import hashlib
import os
import tarfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


@dataclass
class BackupResult:
    archive_path: Path
    encrypted_path: Path
    manifest_path: Path


class BackupService:
    def __init__(
        self,
        backup_dir: Path | str = "backups",
        remote_dir: Optional[Path | str] = None,
    ) -> None:
        self.backup_dir = Path(backup_dir)
        self.remote_dir = Path(remote_dir) if remote_dir else None
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        if self.remote_dir:
            self.remote_dir.mkdir(parents=True, exist_ok=True)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

    def _encrypt_bytes(self, data: bytes, password: str) -> bytes:
        salt = os.urandom(16)
        key = self._derive_key(password, salt)
        token = Fernet(key).encrypt(data)
        return salt + token  # prepend salt for later derivation

    def _decrypt_bytes(self, blob: bytes, password: str) -> bytes:
        salt, token = blob[:16], blob[16:]
        key = self._derive_key(password, salt)
        return Fernet(key).decrypt(token)

    def create_archive(self, name_prefix: str, paths: Iterable[Path | str]) -> Path:
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        archive_path = self.backup_dir / f"{name_prefix}_{timestamp}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tf:
            for p in paths:
                p = Path(p)
                if not p.exists():
                    continue
                tf.add(p, arcname=p.name)
        return archive_path

    def encrypt_archive(self, archive_path: Path, password: str) -> Path:
        encrypted_path = archive_path.with_suffix(archive_path.suffix + ".enc")
        data = archive_path.read_bytes()
        enc = self._encrypt_bytes(data, password)
        encrypted_path.write_bytes(enc)
        return encrypted_path

    def write_manifest(self, encrypted_path: Path) -> Path:
        sha256 = hashlib.sha256(encrypted_path.read_bytes()).hexdigest()
        manifest_path = encrypted_path.with_suffix(encrypted_path.suffix + ".manifest")
        manifest_path.write_text(f"sha256={sha256}\nfilename={encrypted_path.name}\n")
        return manifest_path

    def verify(self, encrypted_path: Path, manifest_path: Path) -> bool:
        expected = None
        for line in manifest_path.read_text().splitlines():
            if line.startswith("sha256="):
                expected = line.split("=", 1)[1].strip()
                break
        if not expected:
            return False
        actual = hashlib.sha256(encrypted_path.read_bytes()).hexdigest()
        return expected == actual

    def upload(self, encrypted_path: Path, manifest_path: Path) -> Optional[List[Path]]:
        if not self.remote_dir:
            return None
        dest_files: List[Path] = []
        for src in (encrypted_path, manifest_path):
            dest = self.remote_dir / src.name
            dest.write_bytes(src.read_bytes())
            dest_files.append(dest)
        return dest_files

    def restore(self, encrypted_path: Path, password: str, target_dir: Path | str) -> Path:
        blob = encrypted_path.read_bytes()
        tar_bytes = self._decrypt_bytes(blob, password)
        temp_tar = encrypted_path.with_suffix(".restore.tmp.tar.gz")
        temp_tar.write_bytes(tar_bytes)
        target = Path(target_dir)
        target.mkdir(parents=True, exist_ok=True)
        with tarfile.open(temp_tar, "r:gz") as tf:
            tf.extractall(path=target)
        temp_tar.unlink(missing_ok=True)
        return target

    def backup(
        self,
        name_prefix: str,
        paths: Iterable[Path | str],
        password: str,
    ) -> BackupResult:
        archive = self.create_archive(name_prefix, paths)
        encrypted = self.encrypt_archive(archive, password)
        manifest = self.write_manifest(encrypted)
        return BackupResult(archive_path=archive, encrypted_path=encrypted, manifest_path=manifest)
