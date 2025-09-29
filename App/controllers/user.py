from ..database import db
from ..models import User, Driver, Resident
from sqlalchemy import func

#get role by id
def get_driver_by_no(driver_no: int) -> Driver | None:
    return Driver.query.filter_by(driver_no=driver_no).first()

def get_resident_by_no(resident_no: int) -> Resident | None:
    return Resident.query.filter_by(resident_no=resident_no).first()

#diff users create
def create_user_basic(username: str, password: str, role: str, street_if_resident: str | None = None):
    """
    Non-interactive user creation for seeding or scripted flows.
    role: "DRIVER" or "RESIDENT"
    """
    if User.query.filter_by(username=username).first():
        return {"error": f'username "{username}" already taken'}

    role = role.upper()
    if role == "DRIVER":
        next_no = (db.session.query(func.max(Driver.driver_no)).scalar() or 0) + 1
        u = Driver(username=username, userType="DRIVER", driver_no=next_no)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return {"message": "driver created", "user": u.toJSON()}

    if role == "RESIDENT":
        if not street_if_resident:
            return {"error": "resident must include a street"}
        next_no = (db.session.query(func.max(Resident.resident_no)).scalar() or 0) + 1
        u = Resident(
            username=username,
            userType="RESIDENT",
            resident_no=next_no,
            street=street_if_resident,
        )
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return {"message": "resident created", "user": u.toJSON()}

    return {"error": 'invalid role (use "DRIVER" or "RESIDENT")'}

def create_user_interactive(username: str, password: str, role: str, street_if_resident: str | None):
    """
    Same as basic, but mirrors the interactive CLI flow (already validated inputs).
    """
    return create_user_basic(username, password, role, street_if_resident)

def create_user(username: str, password: str):
    return create_user_basic(username, password, role="DRIVER")

#list
def list_users_grouped():
    drivers = (
        Driver.query
        .order_by(Driver.driver_no.asc())
        .with_entities(Driver.driver_no, Driver.username)
        .all()
    )
    residents = (
        Resident.query
        .order_by(Resident.resident_no.asc())
        .with_entities(Resident.resident_no, Resident.username, Resident.street)
        .all()
    )
    return {
        "drivers": [{"driverNo": d.driver_no, "username": d.username} for d in drivers],
        "residents": [{"residentNo": r.resident_no, "username": r.username, "street": r.street} for r in residents],
    }