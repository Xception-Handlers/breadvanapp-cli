from ..database import db
from ..models import Drive, StopRequest
from .user import get_resident_by_no, get_driver_by_no
from sqlalchemy import asc, desc


def inbox_for_resident(resident_no: int):
    r = get_resident_by_no(resident_no)
    if not r:
        return {"error": f"resident with id {resident_no} not found"}

    drives = Drive.query.filter_by(street=r.street).order_by(desc(Drive.created_at)).all()
    if not drives:
        return {"inbox": "empty"}

    items = [
        f"Driver with user id {d.driver.driver_no} has scheduled a drive to your street."
        for d in drives
    ]
    return {"inbox": items}


def request_stop_flow(resident_no: int, confirm: bool, chosen_driver_no: int | None, note: str = ""):
    """
    - If confirm is False: return list of drivers who have scheduled drives to the resident's street.
    - If confirm is True: create a StopRequest to the chosen driver for resident's street.
    """
    r = get_resident_by_no(resident_no)
    if not r:
        return {"error": f"resident with id {resident_no} not found"}

    #schedule to streeet drivers
    drives = Drive.query.filter_by(street=r.street).order_by(asc(Drive.created_at)).all()
    unique = {}
    for d in drives:
        drv = d.driver
        if drv.driver_no not in unique:
            unique[drv.driver_no] = drv.username

    driver_list = [{"driverNo": k, "username": v} for k, v in unique.items()]

    if not confirm:
        if not driver_list:
            return {"message": "no drivers scheduled to your street", "drivers": []}
        return {"message": "drivers scheduled to your street", "drivers": driver_list}

    #creatin  request
    if chosen_driver_no is None:
        return {"error": "driver id is required to request a stop"}

    drv = get_driver_by_no(chosen_driver_no)
    if not drv:
        return {"error": f"driver with id {chosen_driver_no} not found"}

    req = StopRequest(resident_id=r.id, driver_id=drv.id, street=r.street, note=note or "")
    db.session.add(req)
    db.session.commit()
    return {"message": "stop request created", "request": req.toJSON()}