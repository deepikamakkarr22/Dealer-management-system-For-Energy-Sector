from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app import mongo

sales_bp = Blueprint("sales", __name__, url_prefix="/sales")


@sales_bp.route("/")
@login_required
def sales_overview():
    # Top 10 dealers by total sales
    top_dealers = list(mongo.db.orders.aggregate([
        {"$match": {"status": {"$in": ["Delivered", "Dispatched"]}}},
        {"$group": {"_id": "$dealer_code", "dealer_name": {"$first": "$dealer_name"},
                    "total_sales": {"$sum": "$total_amount"}, "order_count": {"$sum": 1}}},
        {"$sort": {"total_sales": -1}},
        {"$limit": 10},
    ]))

    # Product-wise sales volume
    product_sales = list(mongo.db.orders.aggregate([
        {"$match": {"status": {"$in": ["Delivered", "Dispatched"]}}},
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.product_code",
            "product_name": {"$first": "$items.product_name"},
            "total_qty": {"$sum": "$items.quantity"},
            "total_revenue": {"$sum": "$items.amount"},
        }},
        {"$sort": {"total_revenue": -1}},
    ]))

    # State-wise revenue
    state_revenue = list(mongo.db.orders.aggregate([
        {"$match": {"status": {"$in": ["Delivered", "Dispatched"]}}},
        {"$lookup": {
            "from": "dealers",
            "localField": "dealer_code",
            "foreignField": "dealer_code",
            "as": "dealer_info",
        }},
        {"$unwind": "$dealer_info"},
        {"$group": {
            "_id": "$dealer_info.contact.state",
            "total_revenue": {"$sum": "$total_amount"},
        }},
        {"$sort": {"total_revenue": -1}},
        {"$limit": 10},
    ]))

    return render_template("sales/overview.html",
                           top_dealers=top_dealers,
                           product_sales=product_sales,
                           state_revenue=state_revenue)
