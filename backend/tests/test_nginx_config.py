from pathlib import Path


def test_userdir_location_block_present():
    content = Path("../config/nginx/sites-available/pubnix-dev").read_text()
    assert "location ~ ^/~(.+?)(/.*)?$" in content
    assert "alias /home/$1/public_html$2" in content


def test_security_headers_present():
    content = Path("../config/nginx/sites-available/pubnix-dev").read_text()
    assert "X-Content-Type-Options" in content
    assert "X-Frame-Options" in content
