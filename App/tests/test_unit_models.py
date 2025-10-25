import pytest
from App.database import db
from App.models import User

@pytest.mark.unit
def test_user_password_hashing(app):
    with app.app_context():
        u = User(username="x", role="DRIVER")
        u.set_password("mypass")
        db.session.add(u); db.session.commit()
        assert u.password_hash != "mypass"
        assert u.check_password("mypass") is True
        assert u.check_password("nope") is False