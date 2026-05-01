"""
Order (indent) collection schema for IOCL DMS.

Collection: orders
"""
from datetime import datetime


ORDER_SCHEMA = {
    "order_no": str,          # "ORD-2024-000123"
    "dealer_id": str,
    "dealer_code": str,
    "dealer_name": str,
    "items": [
        {
            "product_code": str,
            "product_name": str,
            "quantity": float,
            "unit": str,
            "rate_per_unit": float,
            "amount": float,
        }
    ],
    "total_amount": float,
    "status": str,            # "Pending" | "Approved" | "Dispatched" | "Delivered" | "Cancelled"
    "payment_mode": str,      # "Credit" | "Cash" | "DD" | "NEFT"
    "payment_status": str,    # "Paid" | "Unpaid" | "Partial"
    "dispatch_date": datetime,
    "delivery_date": datetime,
    "vehicle_no": str,
    "remarks": str,
    "created_at": datetime,
    "updated_at": datetime,
}
