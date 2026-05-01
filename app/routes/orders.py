from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import mongo
from bson import ObjectId

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/")
@login_required
def list_orders():
    status_filter = request.args.get("status", "")
    payment_filter = request.args.get("payment", "")
    search = request.args.get("q", "")

    query = {}
    if status_filter:
        query["status"] = status_filter
    if payment_filter:
        query["payment_status"] = payment_filter
    if search:
        query["$or"] = [
            {"order_no": {"$regex": search, "$options": "i"}},
            {"dealer_name": {"$regex": search, "$options": "i"}},
        ]

    orders = list(mongo.db.orders.find(query).sort("created_at", -1).limit(100))

    # Status counts for filter pills
    status_counts = list(mongo.db.orders.aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]))

    return render_template("orders/list.html", orders=orders,
                           status_counts=status_counts,
                           status_filter=status_filter,
                           payment_filter=payment_filter, search=search)


@orders_bp.route("/<order_id>")
@login_required
def order_detail(order_id):
    order = mongo.db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        return "Order not found", 404
    dealer = mongo.db.dealers.find_one({"dealer_code": order.get("dealer_code")})
    return render_template("orders/detail.html", order=order, dealer=dealer)


@orders_bp.route("/api/trend")
@login_required
def api_trend():
    pipeline = [
        {"$group": {
            "_id": {
                "year": {"$year": "$created_at"},
                "month": {"$month": "$created_at"},
            },
            "total_amount": {"$sum": "$total_amount"},
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}},
        {"$limit": 12},
    ]
    return jsonify(list(mongo.db.orders.aggregate(pipeline)))
