from pathlib import Path

from services.backup_service import BackupService


def test_backup_and_restore(tmp_path: Path):
    # Arrange test files
    src = tmp_path / "src"
    src.mkdir()
    (src / "file1.txt").write_text("hello")
    (src / "file2.txt").write_text("world")

    svc = BackupService(backup_dir=tmp_path / "backups", remote_dir=tmp_path / "remote")

    # Backup
    res = svc.backup("pubnix", [src], password="testpass")
    assert res.archive_path.exists()
    assert res.encrypted_path.exists()
    assert res.manifest_path.exists()

    # Verify manifest
    assert svc.verify(res.encrypted_path, res.manifest_path) is True

    # Upload (simulated)
    uploaded = svc.upload(res.encrypted_path, res.manifest_path)
    assert uploaded is not None and len(uploaded) == 2

    # Restore
    dest = tmp_path / "restore"
    svc.restore(res.encrypted_path, "testpass", dest)
    assert (dest / "src" / "file1.txt").read_text() == "hello"
    assert (dest / "src" / "file2.txt").read_text() == "world"
