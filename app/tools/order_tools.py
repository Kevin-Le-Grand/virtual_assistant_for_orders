# app/tools/order_tools.py

from langchain.tools import tool
from sqlalchemy import func

from app.models.order import Order


def create_order_tools(user_id):
    """
    Création des Tools associés à l'utilisateur authentifié.

    Le user_id est injecté par Flask et n'est jamais
    contrôlé ou fourni par le LLM.
    """

    def _base_query(status: str | None = None):
        query = Order.query.filter(Order.user_id == user_id)
        if status:
            query = query.filter(func.lower(Order.status) == status.lower())
        return query

    @tool
    def get_orders(status: str | None = None, limit: int = 10):
        """
        Retourne les dernières commandes de l'utilisateur.

        Args:
            status: Statut facultatif pour filtrer les commandes.
            limit: Nombre de commandes à retourner (maximum 20).
        """
        print("========== TOOL get_orders APPELÉ ==========")
        limit = max(1, min(limit, 20))

        orders = (
            _base_query(status)
            .order_by(Order.date_purchase.desc())
            .limit(limit)
            .all()
        )

        return [order.to_dict() for order in orders]

    @tool
    def get_orders_count(status: str | None = None) -> int:
        """
        Retourne le nombre de commandes de l'utilisateur.

        Si aucun statut n'est fourni, retourne le nombre total.
        Sinon, retourne le nombre de commandes ayant ce statut.
        """
        print("--- TOOL GET_ORDERS_COUNT APPELÉ ---")
        total = _base_query(status).count()
        return total

    @tool
    def get_order_by_id(order_id: int):
        """
        Recherche une commande par son identifiant.

        Args:
            order_id: Identifiant de la commande.
        """
        print("========== TOOL get_order_by_id APPELÉ ==========")
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            return {"error": "Commande introuvable."}

        return order.to_dict()

    @tool
    def get_orders_statistics():
        """
        Retourne les statistiques des commandes de l'utilisateur :
        nombre total, nombre par statut, commandes livrées, expédiées
        et non expédiées.
        """
        print("========== TOOL get_orders_statistics APPELÉ ==========")
        base = Order.query.filter(Order.user_id == user_id)

        by_status = dict(
            base.with_entities(Order.status, func.count(Order.id))
            .group_by(Order.status)
            .all()
        )

        return {
            "total_orders": base.count(),
            "orders_by_status": by_status,
            "delivered_orders": base.filter(Order.date_delivered.isnot(None)).count(),
            "shipped_orders": base.filter(Order.date_shipped.isnot(None)).count(),
            "not_shipped_orders": base.filter(Order.date_shipped.is_(None)).count(),
        }

    return [
        get_orders,
        get_orders_count,
        get_order_by_id,
        get_orders_statistics,
    ]