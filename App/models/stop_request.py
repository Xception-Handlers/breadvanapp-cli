from datetime import datetime
from ..database import db


class StopRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    note = db.Column(db.String(255), default="")
    created_at = db.Column(db.String(100), default=lambda: datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))

    def toJSON(self):
        return {
            "id": self.id,
            "residentId": self.resident_id,
            "driverId": self.driver_id,
            "street": self.street,
            "note": self.note,
            "createdAt": self.created_at,
        }