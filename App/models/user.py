from App.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="RESIDENT")

    driver_profile = db.relationship(
        "Driver",
        uselist=False,
        back_populates="user"
    )
    resident = db.relationship("Resident", uselist=False, back_populates="user")

    def __init__(self, username, password=None, role="RESIDENT"):
        self.username = username
        if password:
           self.set_password(password)
        else:
           self.password_hash = ""
        self.role = role.upper()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username
        }
    
    def toJSON(self):
        return self.get_json()
    
    @property
    def password(self):
        return self.password_hash


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_no = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship("User", back_populates="driver_profile")

    def __init__(self, user_id):
        self.user_id = user_id

    def get_json(self):
        return {
            "id": self.id,
            "driver_no": self.driver_no,
            "user_id": self.user_id
        }

class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="resident")
    street = db.Column(db.String, nullable=True)

    @property
    def resident_no(self):
        return self.id
    
from sqlalchemy import event

@event.listens_for(Driver, 'after_insert')
def assign_driver_no(mapper, connection, target):
    
    connection.execute(
        Driver.__table__.update()
        .where(Driver.id == target.id)
        .values(driver_no=target.id)
    )