from .. import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column("order_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False)
    date_purchase = db.Column(db.DateTime, nullable=False)
    date_shipped = db.Column(db.DateTime)
    date_delivered = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="orders")
    
    def to_dict(self):
        return {
            "order_id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "date_purchase": (
                self.date_purchase.isoformat() if self.date_purchase else None
            ),
            "date_shipped": (
                self.date_shipped.isoformat() if self.date_shipped else None
            ),
            "date_delivered": (
                self.date_delivered.isoformat() if self.date_delivered else None
            ),
        }