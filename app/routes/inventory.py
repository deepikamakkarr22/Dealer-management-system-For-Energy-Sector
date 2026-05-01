from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import mongo

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_bp.route("/")
@login_required
def list_inventory():
    product_filter = request.args.get("product", "")
    alert_only = request.args.get("alert", "")

    query = {}
    if product_filter:
        query["product_code"] = product_filter
    if alert_only:
        query["$expr"] = {"$lte": ["$current_stock", "$reorder_level"]}

    items = list(mongo.db.inventory.find(query).sort("dealer_code", 1).limit(200))

    # Summary stats per product
    pipeline = [
        {"$group": {
            "_id": "$product_code",
            "product_name": {"$first": "$product_name"},
            "unit": {"$first": "$unit"},
            "total_stock": {"$sum": "$current_stock"},
            "total_capacity": {"$sum": "$tank_capacity"},
            "low_stock_count": {
                "$sum": {"$cond": [{"$lte": ["$current_stock", "$reorder_level"]}, 1, 0]}
            },
        }},
        {"$sort": {"_id": 1}},
    ]
    summary = list(mongo.db.inventory.aggregate(pipeline))

    return render_template("inventory/list.html", items=items, summary=summary,
                           product_filter=product_filter, alert_only=alert_only)


@inventory_bp.route("/api/levels")
@login_required
def api_levels():
    pipeline = [
        {"$group": {
            "_id": "$product_code",
            "product_name": {"$first": "$product_name"},
            "total_stock": {"$sum": "$current_stock"},
            "total_capacity": {"$sum": "$tank_capacity"},
        }},
        {"$project": {
            "product_name": 1,
            "total_stock": 1,
            "total_capacity": 1,
            "fill_pct": {
                "$multiply": [
                    {"$divide": ["$total_stock", {"$max": ["$total_capacity", 1]}]},
                    100
                ]
            }
        }},
    ]
    return jsonify(list(mongo.db.inventory.aggregate(pipeline)))
