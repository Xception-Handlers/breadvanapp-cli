import pytest
from App.database import db
from App.controllers import (
    create_user, list_users_grouped,
    schedule_drive_by_driver_no, set_status_by_driver_no, get_driver_by_no
)

@pytest.mark.unit
def test_create_user_and_list_grouped(app):
    with app.app_context():
        try: create_user("rob","robpass","DRIVER")
        except Exception: pass
        try: create_user("alice","alicepass","RESIDENT","High Street")
        except Exception: pass
        grouped = list_users_grouped()
        assert len(grouped["drivers"]) >= 1
        assert len(grouped["residents"]) >= 1

@pytest.mark.unit
def test_schedule_and_status_update(app):
    with app.app_context():
        try: create_user("dan","danpass","DRIVER")
        except Exception: pass
        d = get_driver_by_no(1) or get_driver_by_no(2)
        out = schedule_drive_by_driver_no(d.driver_no, "High Street")
        assert "drive" in out
        out2 = set_status_by_driver_no(d.driver_no, "EN_ROUTE", "Gas station")
        assert out2["driver"]["status"] == "EN_ROUTE"