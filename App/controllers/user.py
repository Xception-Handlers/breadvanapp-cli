from __future__ import annotations

from typing import Optional, Dict, List
from sqlalchemy import asc

from App.models import db, User, Resident, Driver


def get_user(user_id: int) -> Optional[User]:
    return db.session.get(User, user_id)


def get_user_by_username(username: str) -> Optional[User]:
    return User.query.filter_by(username=username).first()


def get_driver_by_no(driver_no: int):
    from App.models import Driver
    d = Driver.query.get(driver_no)         
    if d:
        return d
    
    return Driver.query.filter_by(user_id=driver_no).first()


def get_resident_by_no(resident_no: int):
    from App.models import Resident
    r = Resident.query.get(resident_no)
    if r:
        return r
    return Resident.query.filter_by(user_id=resident_no).first()


def create_user(username: str, password: str, role: str = "RESIDENT", street: str = None):
    from App.models import db, User, Resident, Driver

    if not role:
        role = "RESIDENT"
    role = role.upper()

    existing = User.query.filter_by(username=username).first()
    if existing:
        return existing

    u = User(username=username, password=password, role=role)
    db.session.add(u)
    db.session.flush()


    if role == "DRIVER":
        db.session.add(Driver(user_id=u.id))
    else:
        db.session.add(Resident(user_id=u.id, street=street or ""))

    db.session.commit()
    return u


def update_user(user_id: int, new_username: Optional[str] = None) -> User:
    u = get_user(user_id)
    if not u:
        raise ValueError(f"user with id {user_id} not found")
    if new_username:
        if User.query.filter(User.id != user_id, User.username == new_username).first():
            raise ValueError("username already exists")
        u.username = new_username
    db.session.commit()
    return u


def get_all_users_json():
    from App.models import User
    users = User.query.all()
    return [{"id": u.id, "username": u.username} for u in users]




def list_users_grouped() -> Dict[str, List[dict]]:
    """
    Group users by role with keys exactly 'drivers' and 'residents' (tests expect these).
    """
    drivers = [u.get_json() for u in User.query.filter_by(role="DRIVER").order_by(asc(User.id)).all()]
    residents = [u.get_json() for u in User.query.filter_by(role="RESIDENT").order_by(asc(User.id)).all()]
    return {"drivers": drivers, "residents": residents}