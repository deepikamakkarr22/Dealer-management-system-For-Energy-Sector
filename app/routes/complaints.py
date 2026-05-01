from flask import Blueprint, render_template, request
from flask_login import login_required
from app import mongo
from bson import ObjectId

complaints_bp = Blueprint("complaints", __name__, url_prefix="/complaints")


@complaints_bp.route("/")
@login_required
def list_complaints():
    status_filter = request.args.get("status", "")
    category_filter = request.args.get("category", "")

    query = {}
    if status_filter:
        query["status"] = status_filter
    if category_filter:
        query["category"] = category_filter

    complaints = list(mongo.db.complaints.find(query).sort("created_at", -1).limit(100))

    category_counts = list(mongo.db.complaints.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]))

    status_counts = list(mongo.db.complaints.aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]))

    return render_template("complaints/list.html",
                           complaints=complaints,
                           category_counts=category_counts,
                           status_counts=status_counts,
                           status_filter=status_filter,
                           category_filter=category_filter)


@complaints_bp.route("/<complaint_id>")
@login_required
def complaint_detail(complaint_id):
    complaint = mongo.db.complaints.find_one({"_id": ObjectId(complaint_id)})
    if not complaint:
        return "Complaint not found", 404
    dealer = mongo.db.dealers.find_one({"dealer_code": complaint.get("dealer_code")})
    return render_template("complaints/detail.html", complaint=complaint, dealer=dealer)
