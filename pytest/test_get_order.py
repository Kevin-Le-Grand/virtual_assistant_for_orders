from datetime import datetime

from flask_jwt_extended import create_access_token

from app import db
from app.models.order import Order


def create_order(order_id, user_id, status):
    order = Order(
        id=order_id,
        user_id=user_id,
        status=status,
        date_purchase=datetime(2026, 11, 10, 9, 30),
        date_shipped=datetime(2026, 11, 11, 10, 0),
        date_delivered=None,
    )
    db.session.add(order)
    db.session.commit()
    return order


def test_get_orders_returns_only_authenticated_users_orders(app, client):
    with app.app_context():
        order = create_order(23, 7, "shipped")
        create_order(24, 8, "delivered")
        token = create_access_token(identity="7")
        expected = order.to_dict()

    response = client.get(
        "/api/commandes/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == [expected]
    assert expected == {
        "order_id": 23,
        "user_id": 7,
        "status": "shipped",
        "date_purchase": "2026-11-10T09:30:00",
        "date_shipped": "2026-11-11T10:00:00",
        "date_delivered": None,
    }


def test_get_orders_requires_authentication(client):
    response = client.get("/api/commandes/")

    assert response.status_code == 401
