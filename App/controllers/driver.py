from ..database import db
from ..models import Drive, Driver, StopRequest
from .user import get_driver_by_no
from sqlalchemy import desc


def schedule_drive_by_driver_no(driver_no: int, street: str):
    d = get_driver_by_no(driver_no)
    if not d:
        return {"error": f"driver with id {driver_no} not found"}
    drive = Drive(driver_id=d.id, street=street)
    db.session.add(drive)
    db.session.commit()
    return {"message": "drive scheduled", "drive": drive.toJSON()}


def set_status_by_driver_no(driver_no: int, status: str, location: str):
    d = get_driver_by_no(driver_no)
    if not d:
        return {"error": f"driver with id {driver_no} not found"}
    d.status = status.upper()
    d.location = location or ""
    db.session.commit()
    return {"message": "status updated", "driver": d.toJSON()}


def inbox_for_driver(driver_no: int):
    d = get_driver_by_no(driver_no)
    if not d:
        return {"error": f"driver with id {driver_no} not found"}

    requests = (
        StopRequest.query
        .filter_by(driver_id=d.id)
        .order_by(desc(StopRequest.created_at))
        .all()
    )

    if not requests:
        return {"inbox": "empty"}

    items = [
        f"Resident user id {r.resident.resident_no} requested a stop at street '{r.street}'."
        for r in requests
    ]
    return {"inbox": items}