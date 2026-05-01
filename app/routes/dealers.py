from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import mongo
from bson import ObjectId
from datetime import datetime

dealers_bp = Blueprint("dealers", __name__, url_prefix="/dealers")


@dealers_bp.route("/")
@login_required
def list_dealers():
    search = request.args.get("q", "")
    state = request.args.get("state", "")
    status = request.args.get("status", "")
    product_type = request.args.get("product_type", "")

    query = {}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"dealer_code": {"$regex": search, "$options": "i"}},
            {"contact.city": {"$regex": search, "$options": "i"}},
        ]
    if state:
        query["contact.state"] = state
    if status:
        query["status"] = status
    if product_type:
        query["product_type"] = product_type

    dealers = list(mongo.db.dealers.find(query).sort("name", 1).limit(100))
    states = mongo.db.dealers.distinct("contact.state")
    return render_template("dealers/list.html", dealers=dealers, states=sorted(states),
                           search=search, state=state, status=status, product_type=product_type)


@dealers_bp.route("/<dealer_id>")
@login_required
def dealer_detail(dealer_id):
    dealer = mongo.db.dealers.find_one({"_id": ObjectId(dealer_id)})
    if not dealer:
        flash("Dealer not found", "danger")
        return redirect(url_for("dealers.list_dealers"))

    orders = list(mongo.db.orders.find({"dealer_id": dealer_id}).sort("created_at", -1).limit(10))
    inventory = list(mongo.db.inventory.find({"dealer_id": dealer_id}))
    complaints = list(mongo.db.complaints.find({"dealer_id": dealer_id}).sort("created_at", -1).limit(5))

    return render_template("dealers/detail.html",
                           dealer=dealer, orders=orders,
                           inventory=inventory, complaints=complaints)


@dealers_bp.route("/api/stats")
@login_required
def api_stats():
    pipeline = [
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "avg_credit": {"$avg": "$credit_limit"},
            "total_outstanding": {"$sum": "$outstanding_balance"},
        }}
    ]
    result = list(mongo.db.dealers.aggregate(pipeline))
    return jsonify(result)
