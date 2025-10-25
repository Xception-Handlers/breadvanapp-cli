from datetime import datetime
from ..database import db


class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=False)
    street = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="SCHEDULED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    driver = db.relationship("Driver", backref="drives")

    def __init__(self, driver_id, street, status="SCHEDULED"):
        self.driver_id = driver_id
        self.street = street
        self.status = status

    def get_json(self):
        return {
            "id": self.id,
            "driver_id": self.driver_id,
            "street": self.street,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }