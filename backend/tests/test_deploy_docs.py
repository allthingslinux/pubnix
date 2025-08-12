from pathlib import Path

def test_deploy_docs_and_systemd_exist():
    assert Path("../docs/deploy.md").exists()
    assert Path("../infrastructure/systemd/atl-pubnix-backend.service").exists()
    assert Path("../infrastructure/systemd/nginx-reload.service").exists()
    assert Path("../infrastructure/systemd/nginx-reload.timer").exists()
    assert Path("../infrastructure/systemd/atl-pubnix-backend.env.example").exists()
