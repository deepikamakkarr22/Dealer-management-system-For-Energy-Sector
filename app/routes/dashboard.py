from flask import Blueprint, render_template
from flask_login import login_required
from app import mongo
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def home():
    db = mongo.db

    total_dealers = db.dealers.count_documents({})
    active_dealers = db.dealers.count_documents({"status": "Active"})
    pending_orders = db.orders.count_documents({"status": "Pending"})
    open_complaints = db.complaints.count_documents({"status": {"$in": ["Open", "In Progress"]}})

    # Monthly sales volume (KL) for current month
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    pipeline = [
        {"$match": {"created_at": {"$gte": start_of_month}}},
        {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}},
    ]
    sales_agg = list(db.orders.aggregate(pipeline))
    monthly_sales = sales_agg[0]["total"] if sales_agg else 0

    # State-wise dealer count
    state_pipeline = [
        {"$group": {"_id": "$contact.state", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 8},
    ]
    state_data = list(db.dealers.aggregate(state_pipeline))

    # Product-type distribution
    product_pipeline = [
        {"$group": {"_id": "$product_type", "count": {"$sum": 1}}},
    ]
    product_data = list(db.dealers.aggregate(product_pipeline))

    # Last 6 months order trend
    trend = []
    for i in range(5, -1, -1):
        month_start = (datetime.utcnow().replace(day=1) - timedelta(days=30 * i)).replace(
            day=1, hour=0, minute=0, second=0
        )
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        agg = list(db.orders.aggregate([
            {"$match": {"created_at": {"$gte": month_start, "$lt": month_end}}},
            {"$group": {"_id": None, "total": {"$sum": "$total_amount"}, "count": {"$sum": 1}}},
        ]))
        trend.append({
            "label": month_start.strftime("%b %Y"),
            "amount": agg[0]["total"] if agg else 0,
            "count": agg[0]["count"] if agg else 0,
        })

    # Recent orders
    recent_orders = list(db.orders.find().sort("created_at", -1).limit(5))

    # Low stock alerts
    low_stock = list(db.inventory.find(
        {"$expr": {"$lte": ["$current_stock", "$reorder_level"]}}
    ).limit(5))

    return render_template(
        "dashboard/home.html",
        total_dealers=total_dealers,
        active_dealers=active_dealers,
        pending_orders=pending_orders,
        open_complaints=open_complaints,
        monthly_sales=monthly_sales,
        state_data=state_data,
        product_data=product_data,
        trend=trend,
        recent_orders=recent_orders,
        low_stock=low_stock,
    )
