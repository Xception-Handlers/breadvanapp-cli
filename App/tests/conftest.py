import os
import tempfile
import pytest
from App.main import create_app
from App.database import db

@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    db_fd, db_path = tempfile.mkstemp()
    try:
        app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "JWT_SECRET_KEY": "test-secret",
        })
        with app.app_context():
            db.create_all()
        yield app
    finally:
        with app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(db_fd)
        os.remove(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header(app, client):
    from App.controllers import create_user
    with app.app_context():
        try:
            create_user("admin","adminpass","DRIVER")
        except Exception:
            pass
    res = client.post("/api/auth/login", json={"username":"admin","password":"adminpass"})
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}