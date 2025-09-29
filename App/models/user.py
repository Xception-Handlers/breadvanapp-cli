from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ..database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    userType = db.Column(db.String(50), nullable=False)  # noet user driver or resi
    createdAt = db.Column(db.String(100), default=lambda: datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))

    type = db.Column(db.String(50)) 
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "user"}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "userType": self.userType,
            "createdAt": self.createdAt,
        }


class Driver(User):
    __tablename__ = "driver"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    driver_no = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(50), default="OFF_DUTY")  #OFF_DUTY, EN_ROUTE or DELIVERING
    location = db.Column(db.String(255), default="")
    statusUpdatedAt = db.Column(db.String(100), default=lambda: datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))

    drives = db.relationship("Drive", backref="driver", lazy=True)
    stop_requests = db.relationship("StopRequest", backref="driver", lazy=True)

    __mapper_args__ = {"polymorphic_identity": "driver"}

    def toJSON(self):
        data = super().toJSON()
        data.update({
            "driverNo": self.driver_no,
            "status": self.status,
            "location": self.location,
            "statusUpdatedAt": self.statusUpdatedAt,
        })
        return data

    @staticmethod
    def next_driver_no():
        max_no = db.session.query(db.func.max(Driver.driver_no)).scalar()
        return (max_no or 0) + 1


class Resident(User):
    __tablename__ = "resident"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    resident_no = db.Column(db.Integer, unique=True, nullable=False)
    street = db.Column(db.String(120), nullable=False)

    stop_requests = db.relationship("StopRequest", backref="resident", lazy=True)

    __mapper_args__ = {"polymorphic_identity": "resident"}

    def toJSON(self):
        data = super().toJSON()
        data.update({
            "residentNo": self.resident_no,
            "street": self.street,
        })
        return data

    @staticmethod
    def next_resident_no():
        max_no = db.session.query(db.func.max(Resident.resident_no)).scalar()
        return (max_no or 0) + 1

