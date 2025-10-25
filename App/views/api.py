from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.controllers.user import update_user as update_user_ctl
from App.controllers.auth import login
from App.controllers.user import (
    create_user,
    list_users_grouped,
)
from App.controllers.driver import (
    schedule_drive_by_driver_no,
    set_status_by_driver_no,
    inbox_for_driver,
)
from App.controllers.resident import (
    inbox_for_resident,
    request_stop_flow,
)

api = Blueprint("api", __name__, url_prefix="/api")

@api.post("/auth/login")
def api_login():
    data = request.get_json(silent=True) or {}
    token = login(data.get("username", ""), data.get("password", ""))
    if not token:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"access_token": token})

@api.get("/users")
@jwt_required()
def api_users():
    return jsonify(list_users_grouped())

@api.post("/users")
@jwt_required()
def api_create_user():
    data = request.get_json(silent=True) or {}
    try:
        u = create_user(
            username=data["username"],
            password=data["password"],
            role=data["role"],
            street=data.get("street"), 
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(u.toJSON()), 201

@api.post("/drives")
@jwt_required()
def api_schedule_drive():
    data = request.get_json(silent=True) or {}
    driver_no = data.get("driverNo")
    street = data.get("street")
    if not isinstance(driver_no, int) or not street:
        return jsonify({"error": "driverNo (int) and street required"}), 400

    out = schedule_drive_by_driver_no(driver_no, street)  
    return jsonify(out), 201

@api.put("/drivers/<int:driver_no>/status")
@jwt_required()
def api_driver_status(driver_no):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    location = data.get("location")
    if not status:
        return jsonify({"error": "status required"}), 400
    return jsonify(set_status_by_driver_no(driver_no, status, location))

@api.get("/inbox/driver/<int:driver_no>")
@jwt_required()
def api_inbox_driver(driver_no):
    return jsonify(inbox_for_driver(driver_no))

@api.get("/inbox/resident/<int:resident_no>")
@jwt_required()
def api_inbox_resident(resident_no):
    return jsonify(inbox_for_resident(resident_no))

@api.post("/requests")
@jwt_required()
def api_request_stop():
    data = request.get_json(silent=True) or {}
    resident_no = data.get("residentNo")
    chosen_driver_no = data.get("driverNo")  
    note = data.get("note", "")
    confirm = bool(data.get("confirm", False))

    if not isinstance(resident_no, int):
        return jsonify({"error": "residentNo (int) required"}), 400

    return jsonify(
        request_stop_flow(
            resident_no=resident_no,
            confirm=confirm,
            chosen_driver_no=chosen_driver_no,
            note=note,
        )
    ), (201 if confirm else 200)

@api.route("/users/<int:user_id>", methods=["PUT"])   
@jwt_required()
def users_update(user_id: int):                        
    data = request.get_json(silent=True) or {}
    new_username = data.get("username")

    try:
        u = update_user_ctl(user_id, new_username)
        return jsonify(u.get_json()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "update failed"}), 400