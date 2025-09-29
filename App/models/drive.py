from datetime import datetime
from ..database import db


class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(100), default=lambda: datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))

    def toJSON(self):
        return {
            "id": self.id,
            "driverId": self.driver_id,
            "street": self.street,
            "createdAt": self.created_at,
        }