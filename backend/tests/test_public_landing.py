from pathlib import Path


def test_landing_page_exists():
    assert Path("../web/landing/index.html").exists()


def test_nginx_serves_landing():
    content = Path("../config/nginx/sites-available/pubnix-dev").read_text()
    assert "location = /landing" in content
    assert "/opt/pubnix/web/landing/index.html" in content
