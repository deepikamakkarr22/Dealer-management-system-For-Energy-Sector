"""
Inventory collection schema for IOCL DMS.

Collection: inventory
One document per dealer-product combination.
"""
from datetime import datetime


INVENTORY_SCHEMA = {
    "dealer_id": str,
    "dealer_code": str,
    "product_code": str,      # "MS" | "HSD" | "SKO" | "LPG14" | "LPG19"
    "product_name": str,
    "unit": str,              # "KL" | "MT" | "Cylinders"
    "opening_stock": float,
    "current_stock": float,
    "reorder_level": float,
    "last_receipt_date": datetime,
    "last_receipt_qty": float,
    "tank_capacity": float,
    "updated_at": datetime,
}

PRODUCTS = [
    {"code": "MS",    "name": "Motor Spirit (Petrol)", "unit": "KL"},
    {"code": "HSD",   "name": "High Speed Diesel",     "unit": "KL"},
    {"code": "SKO",   "name": "Superior Kerosene Oil",  "unit": "KL"},
    {"code": "LPG14", "name": "LPG 14.2 kg Cylinder",  "unit": "Cylinders"},
    {"code": "LPG19", "name": "LPG 19 kg Cylinder",    "unit": "Cylinders"},
    {"code": "XP95",  "name": "XtraPremium Petrol",     "unit": "KL"},
]
