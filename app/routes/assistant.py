
# app/routes/assistant.py

import logging

from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.services.assistant_service import ask_assistant


assistant_bp = Blueprint(
    "assistant",
    __name__,
    url_prefix="/api/assistant"
)


@assistant_bp.route("/", methods=["POST"])
@jwt_required()
def chat():

    # Récupération de l'identité depuis le JWT vérifié
    user_identity = get_jwt_identity()
    print("Identité utilisateur récupérée :", user_identity)

    # Vérification du type de l'identifiant
    try:
        user_id = int(user_identity)
    except (TypeError, ValueError):
        return jsonify({
            "error": "Identité utilisateur invalide."
        }), 401

    # Récupération du JSON
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Format JSON invalide."
        }), 400

    question = data.get("question")

    # Validation
    if not isinstance(question, str) or not question.strip():
        return jsonify({
            "error": "Veuillez saisir une question."
        }), 400

    question = question.strip()

    if len(question) > 1000:
        return jsonify({
            "error": "La question est trop longue."
        }), 400

    try:
        print("Appel de l'assistant avec la question :", question)
        answer = ask_assistant(
            question=question,
            user_id=user_id
        )
        print("Réponse de l'assistant :", answer)
        return jsonify({
            "answer": answer
        }), 200

    except Exception:

        logging.exception(
            "Erreur pendant l'exécution de l'assistant"
        )

        return jsonify({
            "error": "Une erreur est survenue pendant le traitement."
        }), 500
