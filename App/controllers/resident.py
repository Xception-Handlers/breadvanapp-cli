from ..database import db
from ..models import Drive, StopRequest
from .user import get_resident_by_no, get_driver_by_no
from sqlalchemy import asc, desc

def inbox_for_resident(resident_no: int):
    r = get_resident_by_no(resident_no)
    if not r:
        return {"error": f"resident with id {resident_no} not found"}

    #All drives to the street
    drives = (
        Drive.query
        .filter_by(street=r.street)
        .order_by(desc(Drive.created_at))
        .all()
    )

    items = []

    #keeoing the schedule drive msg
    for d in drives:
        items.append(
            f"Driver with user id {d.driver.driver_no} has scheduled a drive to your street."
        )

    #Include OFF_DUTY, EN_ROUTE, DELIVERING
    seen = set()
    for d in drives:
        drv = d.driver
        if drv.driver_no in seen:
            continue
        seen.add(drv.driver_no)

        status = (drv.status or "").upper()
        if status == "EN_ROUTE":
            status_text = "en route"
        elif status == "DELIVERING":
            status_text = "delivering"
        elif status == "OFF_DUTY":
            status_text = "off duty"
        else:
            continue

        loc_suffix = f" Location: {drv.location}" if drv.location else ""
        items.append(
            f"Driver with user id {drv.driver_no} is {status_text} to your street.{loc_suffix}"
            if status in ("EN_ROUTE", "DELIVERING")
            else f"Driver with user id {drv.driver_no} is {status_text}.{loc_suffix}"
        )

    if not items:
        return {"inbox": "empty"}

    return {"inbox": items}

def request_stop_flow(resident_no: int, confirm: bool, chosen_driver_no: int | None, note: str = ""):
   
    r = get_resident_by_no(resident_no)
    if not r:
        return {"error": f"resident with id {resident_no} not found"}

    #schedule to streeet drivers
    drives = Drive.query.filter_by(street=r.street).order_by(asc(Drive.created_at)).all()
    unique = {}
    for d in drives:
        drv = d.driver
        if drv.driver_no not in unique:
            
            unique[drv.driver_no] = (drv.user.username if drv.user else None)

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

def request_stop(resident_no: int, confirm: bool, chosen_driver_no: int | None, note: str = ""):
    return request_stop_flow(resident_no, confirm, chosen_driver_no, note)