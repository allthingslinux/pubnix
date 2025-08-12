from models import User
from services.provisioning_service import ProvisioningService


def test_build_commands_defaults():
    user = User(username="alice", email="a@example.com", full_name="Alice")
    svc = ProvisioningService(env="production")  # env doesn't affect build
    cmds = svc.build_commands(user)
    assert any("useradd" in c for c in cmds)
    assert f"/home/{user.username}" in " ".join(cmds)
    assert any("public_html" in c for c in cmds)


def test_dry_run_in_dev():
    user = User(username="bob", email="b@example.com", full_name="Bob")
    svc = ProvisioningService(env="development")
    result = svc.provision_user(user)
    assert result.success is True
    assert result.message.startswith("Dry run")
    assert result.commands


def test_production_executes_commands(monkeypatch):
    user = User(username="carol", email="c@example.com", full_name="Carol")
    executed = []

    def fake_runner(argv):
        executed.append(argv)
        return 0

    svc = ProvisioningService(shell_runner=fake_runner, env="production")
    result = svc.provision_user(user, dry_run=False)
    assert result.success is True
    assert executed  # some commands executed
