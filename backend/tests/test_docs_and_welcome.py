from pathlib import Path

from models import User
from services.welcome_service import WelcomeService


def test_docs_files_exist():
    for p in [
        "../docs/user_guide.md",
        "../docs/unix_basics.md",
        "../docs/web_hosting.md",
        "../docs/community_guidelines.md",
    ]:
        assert Path(p).exists()


def test_build_welcome():
    svc = WelcomeService()
    user = User(username="demo", email="d@example.com", full_name="Demo User")
    welcome = svc.build_welcome(user)
    assert "Welcome to ATL Pubnix" in welcome["title"]
    assert "@demo" in welcome["message"]
