from pathlib import Path


def test_fail2ban_jail_defaults():
    p = Path("../config/security/fail2ban/jail.local")
    assert p.exists()
    content = p.read_text()
    assert "[sshd]" in content
    assert "bantime =" in content


def test_apparmor_fcgiwrap_profile():
    p = Path("../config/apparmor/usr.bin.fcgiwrap")
    assert p.exists()
    content = p.read_text()
    assert "/home/**/public_html/**" in content
    assert "deny /etc/**" in content
