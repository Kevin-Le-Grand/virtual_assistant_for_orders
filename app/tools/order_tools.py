
# app/tools/order_tools.py

from itertools import count

from langchain.tools import tool
from sqlalchemy import func

from app.models.order import Order


def create_order_tools(user_id):
    """
    Création des Tools associés à l'utilisateur authentifié.

    Le user_id est injecté par Flask et n'est jamais
    contrôlé ou fourni par le LLM.
    """

    @tool
    def get_orders(status: str = None, limit: int = 10):
        """
        Retourne les dernières commandes de l'utilisateur.

        Args:
            status: Statut facultatif pour filtrer les commandes.
            limit: Nombre de commandes à retourner (maximum 20).
        """
        print("========== TOOL get_orders APPELÉ ==========")
        print("User ID :", user_id)
        print("Status :", status)
        limit = max(1, min(limit, 20))

        orders = (
            Order.query
            .filter_by(user_id=user_id)
            .order_by(Order.date_purchase.desc())
            .limit(limit)
            .all()
        )

        return [
            order.to_dict()
            for order in orders
        ]

    @tool
    def get_orders_count(status: str | None = None) -> int:
        """
        Retourne le nombre de commandes de l'utilisateur.

        Si aucun statut n'est fourni, retourne le nombre total
        de commandes.

        Si un statut est fourni, retourne le nombre de commandes
        correspondant à ce statut.
        """
        print("--- TOOL GET_ORDERS_COUNT APPELÉ ---")

        query = Order.query.filter_by(user_id=user_id)

        if status is not None:
            query = query.filter_by(status=status)

        count = query.count()

        print("Nombre de commandes :", count)

        return count

    @tool
    def get_orders_by_status(status: str, limit: int = 10):
        """
        Retourne les commandes correspondant à un statut.

        Args:
            status: Statut recherché.
            limit: Nombre maximum de résultats (20 maximum).
        """
        print("========== TOOL get_orders_by_status APPELÉ ==========")
        print("User ID :", user_id)
        print("Status :", status)
        limit = max(1, min(limit, 20))

        orders = (
            Order.query
            .filter(
                Order.user_id == user_id,
                func.lower(Order.status) == status.lower()
            )
            .order_by(Order.date_purchase.desc())
            .limit(limit)
            .all()
        )

        return [
            order.to_dict()
            for order in orders
        ]

    @tool
    def get_order_by_id(order_id: int):
        """
        Recherche une commande par son identifiant.

        Args:
            order_id: Identifiant de la commande.
        """
        print("========== TOOL get_order_by_id APPELÉ ==========")
        order = Order.query.filter_by(
            id=order_id,
            user_id=user_id
        ).first()

        if not order:
            return {
                "error": "Commande introuvable."
            }

        return order.to_dict()

    @tool
    def get_orders_statistics():
        """
        Retourne les statistiques des commandes de l'utilisateur :
        nombre total, nombre par statut et nombre de commandes livrées.
        """
        print("========== TOOL get_orders_statistics APPELÉ ==========")
        total = Order.query.filter_by(
            user_id=user_id
        ).count()

        delivered = Order.query.filter(
            Order.user_id == user_id,
            Order.date_delivered.isnot(None)
        ).count()

        shipped = Order.query.filter(
            Order.user_id == user_id,
            Order.date_shipped.isnot(None)
        ).count()

        pending = Order.query.filter(
            Order.user_id == user_id,
            Order.date_shipped.is_(None)
        ).count()

        return {
            "total_orders": total,
            "delivered_orders": delivered,
            "shipped_orders": shipped,
            "not_shipped_orders": pending
        }

    return [
        get_orders,
        get_orders_count,
        get_orders_by_status,
        get_order_by_id,
        get_orders_statistics
    ]
