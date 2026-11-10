from app import db
from app.models.user import User


def create_user():
    user = User(
        prenom="Amina",
        nom="Dupont",
        email="amina.dupont@example.com",
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_login_returns_access_token_for_matching_identity(client, app):
    with app.app_context():
        user = create_user()
        user_id = user.id

    response = client.post(
        "/api/auth/login",
        json={
            "prenom": "Amina",
            "nom": "Dupont",
            "email": "amina.dupont@example.com",
        },
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["access_token"]
    assert body["user"] == {
        "id": user_id,
        "username": "Dupont",
        "email": "amina.dupont@example.com",
    }


def test_login_rejects_non_matching_identity(client, app):
    with app.app_context():
        create_user()

    response = client.post(
        "/api/auth/login",
        json={
            "prenom": "Amina",
            "nom": "Wrong",
            "email": "amina.dupont@example.com",
        },
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "Nom, prénom ou email incorrect"}


def test_login_rejects_missing_fields(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "amina.dupont@example.com"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "email, nom et prenom sont requis"}