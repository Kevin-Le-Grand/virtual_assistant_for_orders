from flask import Blueprint, jsonify, request  
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.order import Order
from .. import db

orders_bp = Blueprint("orders", __name__, url_prefix="/api/commandes")

@orders_bp.route("/", methods=["GET"])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_dict() for order in orders]), 200