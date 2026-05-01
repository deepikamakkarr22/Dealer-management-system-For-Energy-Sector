"""
Dealer collection schema for IOCL DMS.

Collection: dealers
Indexes: dealer_code (unique), state, product_type, status
"""
from datetime import datetime


DEALER_SCHEMA = {
    "dealer_code": str,       # e.g. "IOCL-DL-0042"
    "name": str,
    "owner_name": str,
    "contact": {
        "phone": str,
        "email": str,
        "address": str,
        "city": str,
        "state": str,
        "pincode": str,
    },
    "product_type": str,      # "Petrol & Diesel" | "LPG" | "Lubricants" | "Multi"
    "territory": str,
    "license_no": str,
    "license_expiry": datetime,
    "onboarded_on": datetime,
    "status": str,            # "Active" | "Inactive" | "Suspended"
    "credit_limit": float,
    "outstanding_balance": float,
    "assigned_ro": str,       # Regional Office code
    "kpis": {
        "monthly_volume_kl": float,
        "customer_rating": float,
        "compliance_score": float,
    },
    "created_at": datetime,
    "updated_at": datetime,
}


def dealer_summary(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "dealer_code": doc.get("dealer_code"),
        "name": doc.get("name"),
        "city": doc.get("contact", {}).get("city"),
        "state": doc.get("contact", {}).get("state"),
        "product_type": doc.get("product_type"),
        "status": doc.get("status"),
        "credit_limit": doc.get("credit_limit", 0),
        "outstanding_balance": doc.get("outstanding_balance", 0),
    }
