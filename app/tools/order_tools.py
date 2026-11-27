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


    return [
        get_orders,
        get_orders_count,
    ]