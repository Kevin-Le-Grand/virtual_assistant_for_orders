from .. import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = "users"

    id = db.Column("user_id", db.Integer, primary_key=True)
    prenom = db.Column("first_name", db.String(100), nullable=False)
    nom = db.Column("last_name", db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)