
from __future__ import annotations

import re
from contextlib import suppress
from flask import current_app, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash

from App.database import db
from App.models.user import User


def setup_jwt(app):
    
    JWTManager(app)

def login(username, password):
    from App.models import User
    from flask_jwt_extended import create_access_token

    app = current_app._get_current_object() if current_app else None
    if app and not app.config.get("JWT_SECRET_KEY"):
        app.config["JWT_SECRET_KEY"] = "test-secret"

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=str(user.id))
    return None

def authenticate():
    
    return jwt_required()


def current_user() -> User | None:
    
    with suppress(Exception):
        uid = get_jwt_identity()
        if uid is None:
            return None
        return db.session.get(User, int(uid))
    return None


def add_auth_context(app):
    return app


def _extract_access_token_weird_bearer(value: str) -> str | None:
    
    m = re.search(r"access_token[\"']?\s*:\s*[\"']([^\"']+)[\"']", value)
    if m:
        return m.group(1)

    
    m2 = re.search(r"eyJ[^\"'\s}]+", value)
    return m2.group(0) if m2 else None


def add_auth_header_normalizer(app):
    
    @app.before_request
    def _normalize_bearer_header():
        auth = request.headers.get("Authorization")
        if not auth:
            return
        if auth.startswith("Bearer ") and "access_token" in auth:
            
            token = _extract_access_token_weird_bearer(auth)
            if token:
                
                request.environ["HTTP_AUTHORIZATION"] = f"Bearer {token}"

from flask import request


def add_auth_header_normalizer(app):
    
    @app.before_request
    def normalize_header():
        if "Authorization" not in request.headers and "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            request.headers.environ["HTTP_AUTHORIZATION"] = f"Bearer {token}"


def add_auth_context(app):
    
    pass