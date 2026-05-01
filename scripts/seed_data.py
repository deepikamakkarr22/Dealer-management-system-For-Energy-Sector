"""
Seed script — populates MongoDB with realistic IOCL demo data.

Usage:
    python scripts/seed_data.py

Requires MONGO_URI in .env or defaults to mongodb://localhost:27017/iocl_dms
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

import random
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING
from faker import Faker
import bcrypt

fake = Faker("en_IN")
random.seed(42)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/iocl_dms")
client = MongoClient(MONGO_URI)
db = client.get_default_database()

# ── Config ─────────────────────────────────────────────────────────────
NUM_DEALERS    = 60
NUM_ORDERS     = 400
NUM_COMPLAINTS = 80

STATES = ["Uttar Pradesh","Maharashtra","Rajasthan","Gujarat","Madhya Pradesh",
          "Karnataka","Tamil Nadu","West Bengal","Andhra Pradesh","Punjab",
          "Haryana","Bihar","Odisha","Telangana","Kerala"]

CITIES = {
    "Uttar Pradesh": ["Lucknow","Kanpur","Agra","Varanasi","Noida"],
    "Maharashtra":   ["Mumbai","Pune","Nagpur","Nashik","Aurangabad"],
    "Rajasthan":     ["Jaipur","Jodhpur","Udaipur","Kota","Ajmer"],
    "Gujarat":       ["Ahmedabad","Surat","Vadodara","Rajkot","Gandhinagar"],
    "Madhya Pradesh":["Bhopal","Indore","Gwalior","Jabalpur","Ujjain"],
    "Karnataka":     ["Bengaluru","Mysuru","Hubli","Mangaluru","Belagavi"],
    "Tamil Nadu":    ["Chennai","Coimbatore","Madurai","Tiruchirappalli","Salem"],
    "West Bengal":   ["Kolkata","Howrah","Durgapur","Asansol","Siliguri"],
    "Andhra Pradesh":["Visakhapatnam","Vijayawada","Guntur","Nellore","Kurnool"],
    "Punjab":        ["Ludhiana","Amritsar","Jalandhar","Patiala","Bathinda"],
    "Haryana":       ["Gurugram","Faridabad","Panipat","Ambala","Karnal"],
    "Bihar":         ["Patna","Gaya","Bhagalpur","Muzaffarpur","Darbhanga"],
    "Odisha":        ["Bhubaneswar","Cuttack","Rourkela","Berhampur","Sambalpur"],
    "Telangana":     ["Hyderabad","Warangal","Nizamabad","Karimnagar","Khammam"],
    "Kerala":        ["Thiruvananthapuram","Kochi","Kozhikode","Thrissur","Kollam"],
}

PRODUCT_TYPES = ["Petrol & Diesel", "LPG", "Lubricants", "Multi"]
PRODUCTS = [
    {"code":"MS",    "name":"Motor Spirit (Petrol)",   "unit":"KL",        "rate": 95000},
    {"code":"HSD",   "name":"High Speed Diesel",       "unit":"KL",        "rate": 87000},
    {"code":"SKO",   "name":"Superior Kerosene Oil",   "unit":"KL",        "rate": 72000},
    {"code":"LPG14", "name":"LPG 14.2 kg Cylinder",   "unit":"Cylinders", "rate": 900},
    {"code":"LPG19", "name":"LPG 19 kg Cylinder",      "unit":"Cylinders", "rate": 1800},
    {"code":"XP95",  "name":"XtraPremium Petrol",      "unit":"KL",        "rate": 102000},
]

COMPLAINT_CATEGORIES = ["Fuel Quality","Supply Delay","Billing Issue",
                         "Equipment Failure","Staff Conduct","Pricing Dispute","Other"]
COMPLAINT_SUBJECTS = {
    "Fuel Quality":     ["Adulterated petrol reported","Diesel quality substandard","Water contamination in tank"],
    "Supply Delay":     ["Tanker delay of 3 days","No supply for 48 hours","Last mile delivery delayed"],
    "Billing Issue":    ["Incorrect invoice amount","GST mismatch on bill","Duplicate charge raised"],
    "Equipment Failure":["Dispenser not working","Flow meter faulty","DG set failure"],
    "Staff Conduct":    ["Rude behaviour by staff","Overcharging customers","Uniform non-compliance"],
    "Pricing Dispute":  ["Retail price board outdated","Overcharging on LPG","Credit note not issued"],
    "Other":            ["CCTV not functional","Signage missing","Toilet facility issue"],
}

ROS = ["RO-North","RO-South","RO-East","RO-West","RO-Central"]


def rand_date(start_days_ago=730, end_days_ago=0):
    start = datetime.utcnow() - timedelta(days=start_days_ago)
    end   = datetime.utcnow() - timedelta(days=end_days_ago)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


def drop_collections():
    for col in ["users","dealers","inventory","orders","complaints"]:
        db[col].drop()
    print("  Dropped existing collections.")


def create_indexes():
    db.dealers.create_index([("dealer_code", ASCENDING)], unique=True)
    db.dealers.create_index([("contact.state", ASCENDING)])
    db.dealers.create_index([("status", ASCENDING)])
    db.orders.create_index([("order_no", ASCENDING)], unique=True)
    db.orders.create_index([("dealer_code", ASCENDING)])
    db.orders.create_index([("created_at", ASCENDING)])
    db.inventory.create_index([("dealer_id", ASCENDING), ("product_code", ASCENDING)])
    db.complaints.create_index([("dealer_code", ASCENDING)])
    db.complaints.create_index([("status", ASCENDING)])
    print("  Created indexes.")


def seed_users():
    users = [
        {"username":"admin",   "email":"admin@iocl.in",   "role":"admin",   "full_name":"Admin User"},
        {"username":"manager", "email":"mgr@iocl.in",     "role":"manager", "full_name":"Regional Manager"},
        {"username":"viewer",  "email":"viewer@iocl.in",  "role":"viewer",  "full_name":"View Only User"},
    ]
    for u in users:
        pw = "admin123" if u["username"] == "admin" else u["username"] + "123"
        u["password_hash"] = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        db.users.insert_one(u)
    print(f"  Seeded {len(users)} users.")


def seed_dealers():
    dealers = []
    for i in range(1, NUM_DEALERS + 1):
        state = random.choice(STATES)
        city  = random.choice(CITIES[state])
        pt    = random.choice(PRODUCT_TYPES)
        status = random.choices(["Active","Active","Active","Inactive","Suspended"],
                                weights=[70,70,70,15,5])[0]
        credit = round(random.uniform(500000, 5000000), -3)
        outstanding = round(random.uniform(0, credit * 0.9), -2)
        dealer = {
            "dealer_code": f"IOCL-{state[:2].upper()}-{i:04d}",
            "name": f"{fake.last_name()} {random.choice(['Fuel Centre','Petroleum','Energy Hub','Service Station','Auto Fuels'])}",
            "owner_name": fake.name(),
            "contact": {
                "phone":   fake.phone_number(),
                "email":   fake.email(),
                "address": fake.street_address(),
                "city":    city,
                "state":   state,
                "pincode": fake.postcode(),
            },
            "product_type": pt,
            "territory":    f"{city} Zone",
            "license_no":   f"LIC-{state[:3].upper()}-{random.randint(10000,99999)}",
            "license_expiry": rand_date(0, -365),
            "onboarded_on":   rand_date(3650, 30),
            "status":   status,
            "credit_limit":   credit,
            "outstanding_balance": outstanding,
            "assigned_ro": random.choice(ROS),
            "kpis": {
                "monthly_volume_kl": round(random.uniform(50, 800), 1),
                "customer_rating":   round(random.uniform(2.5, 5.0), 1),
                "compliance_score":  round(random.uniform(40, 100), 1),
            },
            "created_at": rand_date(3650, 30),
            "updated_at": rand_date(30, 0),
        }
        dealers.append(dealer)
    db.dealers.insert_many(dealers)
    print(f"  Seeded {len(dealers)} dealers.")
    return list(db.dealers.find({}, {"_id":1,"dealer_code":1,"name":1,"product_type":1}))


def seed_inventory(dealers):
    inv = []
    for d in dealers:
        # Pick 2–4 products per dealer
        prods = random.sample(PRODUCTS, k=random.randint(2, 4))
        for p in prods:
            capacity = round(random.uniform(10000, 80000) if p["unit"] == "KL"
                             else random.uniform(500, 5000), 0)
            reorder  = round(capacity * random.uniform(0.1, 0.25), 0)
            current  = round(random.uniform(0, capacity), 0)
            inv.append({
                "dealer_id":        str(d["_id"]),
                "dealer_code":      d["dealer_code"],
                "product_code":     p["code"],
                "product_name":     p["name"],
                "unit":             p["unit"],
                "opening_stock":    current,
                "current_stock":    current,
                "reorder_level":    reorder,
                "tank_capacity":    capacity,
                "last_receipt_date": rand_date(60, 1),
                "last_receipt_qty":  round(random.uniform(reorder, capacity * 0.5), 1),
                "updated_at":        datetime.utcnow(),
            })
    db.inventory.insert_many(inv)
    print(f"  Seeded {len(inv)} inventory records.")


def seed_orders(dealers):
    orders = []
    statuses = ["Pending","Approved","Dispatched","Delivered","Delivered","Delivered","Cancelled"]
    pmodes   = ["Credit","Cash","DD","NEFT"]
    for i in range(1, NUM_ORDERS + 1):
        d = random.choice(dealers)
        created = rand_date(365, 0)
        status  = random.choice(statuses)
        items   = []
        total   = 0
        for p in random.sample(PRODUCTS, k=random.randint(1, 3)):
            qty  = round(random.uniform(1, 50) if p["unit"] == "KL" else random.uniform(50, 500), 1)
            rate = p["rate"] * random.uniform(0.97, 1.03)
            amt  = round(qty * rate, 2)
            total += amt
            items.append({
                "product_code":  p["code"],
                "product_name":  p["name"],
                "quantity":      qty,
                "unit":          p["unit"],
                "rate_per_unit": round(rate, 2),
                "amount":        amt,
            })
        pstatus = "Paid" if status == "Delivered" else random.choice(["Paid","Unpaid","Partial"])
        dispatch = created + timedelta(days=random.randint(1,3)) if status in ["Dispatched","Delivered"] else None
        delivery = dispatch + timedelta(days=random.randint(1,2)) if status == "Delivered" and dispatch else None
        orders.append({
            "order_no":       f"ORD-{created.year}-{i:06d}",
            "dealer_id":      str(d["_id"]),
            "dealer_code":    d["dealer_code"],
            "dealer_name":    d["name"],
            "items":          items,
            "total_amount":   round(total, 2),
            "status":         status,
            "payment_mode":   random.choice(pmodes),
            "payment_status": pstatus,
            "dispatch_date":  dispatch,
            "delivery_date":  delivery,
            "vehicle_no":     f"UP{random.randint(10,99)}G{random.randint(1000,9999)}" if dispatch else None,
            "remarks":        "",
            "created_at":     created,
            "updated_at":     created + timedelta(hours=random.randint(1,48)),
        })
    db.orders.insert_many(orders)
    print(f"  Seeded {len(orders)} orders.")


def seed_complaints(dealers):
    complaints = []
    statuses  = ["Open","In Progress","Resolved","Resolved","Closed"]
    priorities = ["High","Medium","Medium","Low"]
    for i in range(1, NUM_COMPLAINTS + 1):
        d        = random.choice(dealers)
        cat      = random.choice(COMPLAINT_CATEGORIES)
        subject  = random.choice(COMPLAINT_SUBJECTS[cat])
        status   = random.choice(statuses)
        created  = rand_date(180, 0)
        resolved = created + timedelta(days=random.randint(2,14)) if status in ["Resolved","Closed"] else None
        complaints.append({
            "ref_no":       f"CMP-{created.year}-{i:04d}",
            "dealer_id":    str(d["_id"]),
            "dealer_code":  d["dealer_code"],
            "dealer_name":  d["name"],
            "category":     cat,
            "subject":      subject,
            "description":  fake.paragraph(nb_sentences=3),
            "priority":     random.choice(priorities),
            "status":       status,
            "assigned_to":  fake.name() if status != "Open" else None,
            "resolution":   fake.sentence() if status in ["Resolved","Closed"] else None,
            "created_at":   created,
            "updated_at":   resolved or created,
            "resolved_at":  resolved,
        })
    db.complaints.insert_many(complaints)
    print(f"  Seeded {len(complaints)} complaints.")


if __name__ == "__main__":
    print("\n🛢  IOCL DMS — MongoDB Seed Script")
    print("=" * 45)
    drop_collections()
    create_indexes()
    seed_users()
    dealer_docs = seed_dealers()
    seed_inventory(dealer_docs)
    seed_orders(dealer_docs)
    seed_complaints(dealer_docs)
    print("=" * 45)
    print("✅  Seed complete! Login: admin / admin123\n")
