
from __future__ import annotations

from typing import Dict, List
from sqlalchemy import asc
from App.database import db
from App.models.user import Driver
from App.models.drive import Drive
from App.models import db, Drive, Driver, User


def schedule_drive_by_driver_no(driver_no: int, street: str) -> dict:
   
    driver = Driver.query.filter_by(driver_no=driver_no).first()
    if not driver:
        raise ValueError(f"driver {driver_no} not found")
    d = Drive(driver_id=driver.id, street=street, status="SCHEDULED")
    db.session.add(d)
    db.session.commit()
    return {
        "drive": {
            "id": d.id,
            "driverNo": driver.driver_no,
            "street": d.street,
            "status": d.status,
        }
    }

def get_driver_by_no(driver_no: int):
    return Driver.query.get(driver_no)

def set_status_by_driver_no(driver_no: int, status: str, location: Optional[str] = None) -> dict:
    
    driver = Driver.query.filter_by(driver_no=driver_no).first()
    if not driver:
        raise ValueError(f"driver {driver_no} not found")

    
    changed = False
    if hasattr(driver, "status"):
        driver.status = status
        changed = True
    if hasattr(driver, "location"):
        driver.location = location
        changed = True
    if changed:
        db.session.commit()

    return {
        "driver": {
            "driverNo": driver.driver_no,
            "status": status,
            "location": location,
        }
    }


def inbox_for_driver(driver_no: int) -> dict:
    
    driver = Driver.query.filter_by(driver_no=driver_no).first()
    if not driver:
        raise ValueError(f"driver {driver_no} not found")
    return {"requests": [], "notifications": []}