from .. import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = "users"

    id = db.Column("user_id", db.Integer, primary_key=True)
    prenom = db.Column("first_name", db.String(100), nullable=False)
    nom = db.Column("last_name", db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telephone = db.Column("phone", db.String(20), nullable=True)
    adresse = db.Column("address", db.String(255), nullable=True)
    ville = db.Column("city", db.String(100), nullable=True)
    code_postal = db.Column("zip_code", db.String(20), nullable=True)
    date_creation = db.Column("joining_date", db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "prenom": self.prenom,
            "nom": self.nom,
            "email": self.email,
            "telephone": self.telephone,
            "adresse": self.adresse,
            "ville": self.ville,
            "code_postal": self.code_postal,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None,
        }