from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app import mongo
from datetime import datetime, timedelta

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/")
@login_required
def reports_home():
    # KPI summary
    total_revenue = list(mongo.db.orders.aggregate([
        {"$match": {"status": {"$in": ["Delivered", "Dispatched"]}}},
        {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}},
    ]))
    revenue = total_revenue[0]["total"] if total_revenue else 0

    avg_order_value = list(mongo.db.orders.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$total_amount"}}},
    ]))
    avg_order = avg_order_value[0]["avg"] if avg_order_value else 0

    # Dealer compliance scores
    compliance = list(mongo.db.dealers.aggregate([
        {"$group": {
            "_id": "$contact.state",
            "avg_compliance": {"$avg": "$kpis.compliance_score"},
            "avg_rating": {"$avg": "$kpis.customer_rating"},
        }},
        {"$sort": {"avg_compliance": -1}},
        {"$limit": 10},
    ]))

    # Monthly revenue for chart
    monthly = []
    for i in range(11, -1, -1):
        start = (datetime.utcnow().replace(day=1) - timedelta(days=30 * i)).replace(
            day=1, hour=0, minute=0, second=0)
        end = (start + timedelta(days=32)).replace(day=1)
        agg = list(mongo.db.orders.aggregate([
            {"$match": {"created_at": {"$gte": start, "$lt": end},
                        "status": {"$in": ["Delivered", "Dispatched"]}}},
            {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}},
        ]))
        monthly.append({
            "label": start.strftime("%b %y"),
            "value": round(agg[0]["total"] / 1e6, 2) if agg else 0,
        })

    return render_template("reports/home.html",
                           revenue=revenue,
                           avg_order=avg_order,
                           compliance=compliance,
                           monthly=monthly)
