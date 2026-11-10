from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Aucune donnée reçue"}), 400

    email = data.get("email")
    nom = data.get("nom")
    prenom = data.get("prenom")

    if not email or not nom or not prenom:
        return jsonify({"error": "email, nom et prenom sont requis"}), 400

    user = User.query.filter_by(email=email, nom=nom, prenom=prenom).first()

    if not user:
        return jsonify({"error": "Nom, prénom ou email incorrect"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=15),
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.nom,
            "email": user.email,
        }
    }), 200