from pathlib import Path


def test_terraform_and_ansible_present():
    assert Path("../infrastructure/terraform/hetzner/main.tf").exists()
    assert Path("../infrastructure/ansible/site.yml").exists()
    assert Path("../infrastructure/ansible/roles/sshd/tasks/main.yml").exists()
    assert Path("../infrastructure/ansible/roles/nginx/tasks/main.yml").exists()
    assert Path("../infrastructure/ansible/roles/common/tasks/main.yml").exists()
