"""
seed_demo_data.py — MongoDB for Relational Developers (Demo Dataset)
=====================================================================

Seeds the 'shop' database with realistic e-commerce data that matches
every live demo query in the presentation exactly.

Collections created
───────────────────
  customers     60 docs   APAC · EMEA · AMER  ×  gold · silver · bronze
  orders       ~300 docs   embedded items · custId reference · all statuses
  inventory     10 docs   stock quantities  (sku "A1" qty=2 for txn demo)
  audit_log      0 docs   empty — written live during Demo 6 (Transactions)
  orders_large  500K docs  lean docs used for Demo 4 (Index before & after)

Prerequisites
─────────────
  pip install pymongo faker

Usage
─────
  python seed_demo_data.py                               # localhost:27017
  python seed_demo_data.py --uri "mongodb+srv://..."     # Atlas
  python seed_demo_data.py --uri <uri> --db mydb         # custom DB name
  python seed_demo_data.py --skip-large                  # skip 500K insert
  python seed_demo_data.py --drop                        # drop DB first
"""

import argparse
import random
import sys
import time
from datetime import datetime, timedelta

from bson import ObjectId
from faker import Faker
from pymongo import MongoClient, ASCENDING

# ── Reproducible randomness ────────────────────────────────────────────────────
fake = Faker()
Faker.seed(42)
random.seed(42)


# ══════════════════════════════════════════════════════════════════════════════
# REFERENCE DATA
# ══════════════════════════════════════════════════════════════════════════════

REGIONS  = ["APAC", "EMEA", "AMER"]
TIERS    = ["gold", "silver", "bronze"]
STATUSES = (["completed"] * 4 + ["shipped"] * 3 +
            ["pending"]   * 2 + ["cancelled"] * 1)   # weighted distribution

# 10 product SKUs — used in both orders (embedded items) and inventory
PRODUCTS = [
    {"sku": "A1", "name": "Wireless Mouse",         "unitPrice": 49.99},
    {"sku": "B3", "name": "USB-C Hub",              "unitPrice": 79.99},
    {"sku": "C5", "name": "Laptop Stand",           "unitPrice": 39.99},
    {"sku": "D7", "name": "Mechanical Keyboard",    "unitPrice": 129.99},
    {"sku": "E2", "name": "27-inch Monitor",        "unitPrice": 349.99},
    {"sku": "F6", "name": "Webcam HD",              "unitPrice": 89.99},
    {"sku": "G9", "name": "Desk Lamp LED",          "unitPrice": 34.99},
    {"sku": "H4", "name": "Cable Organiser Set",    "unitPrice": 14.99},
    {"sku": "I8", "name": "Ergonomic Chair Cushion","unitPrice": 59.99},
    {"sku": "J2", "name": "Monitor Arm",            "unitPrice": 74.99},
]
PRODUCT_MAP = {p["sku"]: p for p in PRODUCTS}

# ── Hero customers — fixed ObjectIds so Demo 1 queries work reliably ──────────
# These IDs are printed in the cheat-sheet at the end of seeding.
HERO_IDS = {
    "alice":  ObjectId("665f000000000000000001a1"),
    "bob":    ObjectId("665f000000000000000001b2"),
    "carol":  ObjectId("665f000000000000000001c3"),
    "david":  ObjectId("665f000000000000000001d4"),
}

HERO_CUSTOMERS = [
    {"_id": HERO_IDS["alice"], "name": "Alice Chen",
     "email": "alice.chen@example.com",  "region": "APAC", "tier": "gold",
     "phone": "+65 9123 4567", "createdAt": datetime(2022, 3, 15)},

    {"_id": HERO_IDS["bob"],   "name": "Bob Patel",
     "email": "bob.patel@example.com",   "region": "EMEA", "tier": "silver",
     "phone": "+44 7700 900123", "createdAt": datetime(2022, 5, 22)},

    {"_id": HERO_IDS["carol"], "name": "Carol Smith",
     "email": "carol.smith@example.com", "region": "AMER", "tier": "gold",
     "phone": "+1 415 555 0198", "createdAt": datetime(2021, 11, 8)},

    {"_id": HERO_IDS["david"], "name": "David Kim",
     "email": "david.kim@example.com",   "region": "APAC", "tier": "bronze",
     "phone": "+82 10 1234 5678", "createdAt": datetime(2023, 1, 30)},
]


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def rand_date(days_back: int = 730) -> datetime:
    """Return a random UTC datetime within the last `days_back` days."""
    return datetime.utcnow() - timedelta(days=random.randint(0, days_back))


def make_items(n: int = None) -> list:
    """Build n embedded order line-items from the product catalogue."""
    n = n or random.randint(1, 4)
    chosen = random.sample(PRODUCTS, min(n, len(PRODUCTS)))
    return [
        {
            "sku":       p["sku"],
            "name":      p["name"],
            "qty":       random.randint(1, 4),
            "unitPrice": p["unitPrice"],
        }
        for p in chosen
    ]


def calc_amount(items: list) -> float:
    """Sum qty × unitPrice across embedded items, rounded to 2 dp."""
    return round(sum(i["qty"] * i["unitPrice"] for i in items), 2)


def progress(label: str, current: int, total: int, width: int = 40) -> None:
    filled = int(width * current / total)
    bar    = "█" * filled + "░" * (width - filled)
    pct    = current / total * 100
    print(f"\r  {label}: [{bar}] {pct:5.1f}%  ({current:,}/{total:,})",
          end="", flush=True)


# ══════════════════════════════════════════════════════════════════════════════
# SEEDERS
# ══════════════════════════════════════════════════════════════════════════════

def seed_customers(db) -> list:
    """
    Seed 60 customers:
      - 4 hero customers with fixed ObjectIds (used in demo queries)
      - 56 generated customers evenly spread across regions × tiers
    Returns the full list of customer documents.
    """
    print("\n[1/5] Seeding customers …")
    db.customers.drop()

    extra = []
    per_region_tier = 56 // (len(REGIONS) * len(TIERS))   # ≈ 6 each → 54, pad to 56

    for region in REGIONS:
        for tier in TIERS:
            for _ in range(per_region_tier):
                extra.append({
                    "_id":       ObjectId(),
                    "name":      fake.name(),
                    "email":     fake.unique.email(),
                    "region":    region,
                    "tier":      tier,
                    "phone":     fake.phone_number()[:20],
                    "createdAt": rand_date(1095),   # up to 3 years ago
                })
    # pad to exactly 56
    while len(extra) < 56:
        extra.append({
            "_id":       ObjectId(),
            "name":      fake.name(),
            "email":     fake.unique.email(),
            "region":    random.choice(REGIONS),
            "tier":      random.choice(TIERS),
            "phone":     fake.phone_number()[:20],
            "createdAt": rand_date(1095),
        })

    all_customers = HERO_CUSTOMERS + extra
    db.customers.insert_many(all_customers)
    print(f"\r  ✅  {len(all_customers)} customers inserted")
    return all_customers


def seed_orders(db, customers: list) -> None:
    """
    Seed ~300 orders with embedded line-items.
    Each customer gets 3–7 orders so aggregation results are interesting.
    Hero customers always have orders covering multiple statuses.
    """
    print("\n[2/5] Seeding orders …")
    db.orders.drop()

    orders = []

    # ── Hero orders (match Demo 1 slide exactly) ──────────────────────────────
    hero_orders = [
        # Alice — 2 completed, 1 pending
        {
            "_id":       ObjectId("665f000000000000000002a1"),
            "custId":    HERO_IDS["alice"],
            "status":    "completed",
            "items":     [{"sku":"A1","name":"Wireless Mouse","qty":2,"unitPrice":49.99},
                          {"sku":"B3","name":"USB-C Hub",     "qty":1,"unitPrice":79.99}],
            "amount":    179.97,
            "createdAt": datetime(2024, 1, 15),
        },
        {
            "_id":       ObjectId("665f000000000000000002a2"),
            "custId":    HERO_IDS["alice"],
            "status":    "completed",
            "items":     [{"sku":"D7","name":"Mechanical Keyboard","qty":1,"unitPrice":129.99}],
            "amount":    129.99,
            "createdAt": datetime(2024, 2, 8),
        },
        {
            "_id":       ObjectId("665f000000000000000002a3"),
            "custId":    HERO_IDS["alice"],
            "status":    "pending",
            "items":     [{"sku":"A1","name":"Wireless Mouse","qty":1,"unitPrice":49.99},
                          {"sku":"D7","name":"Mechanical Keyboard","qty":1,"unitPrice":129.99}],
            "amount":    179.98,
            "createdAt": datetime(2024, 3, 1),
        },
        # Bob — 1 completed
        {
            "_id":       ObjectId("665f000000000000000002b1"),
            "custId":    HERO_IDS["bob"],
            "status":    "completed",
            "items":     [{"sku":"C5","name":"Laptop Stand","qty":3,"unitPrice":39.99}],
            "amount":    119.97,
            "createdAt": datetime(2024, 2, 20),
        },
        # Carol — 1 completed (high-value, good for aggregation)
        {
            "_id":       ObjectId("665f000000000000000002c1"),
            "custId":    HERO_IDS["carol"],
            "status":    "completed",
            "items":     [{"sku":"E2","name":"27-inch Monitor","qty":2,"unitPrice":349.99}],
            "amount":    699.98,
            "createdAt": datetime(2024, 3, 10),
        },
        # David — 1 completed (low-value bronze tier)
        {
            "_id":       ObjectId("665f000000000000000002d1"),
            "custId":    HERO_IDS["david"],
            "status":    "completed",
            "items":     [{"sku":"C5","name":"Laptop Stand","qty":1,"unitPrice":39.99}],
            "amount":    39.99,
            "createdAt": datetime(2024, 4, 5),
        },
    ]

    orders.extend(hero_orders)

    # ── Generated orders for all 60 customers ────────────────────────────────
    for cust in customers:
        n_orders = random.randint(3, 7)
        for _ in range(n_orders):
            status    = random.choice(STATUSES)
            items     = make_items()
            amount    = calc_amount(items)
            created   = rand_date(730)
            doc = {
                "_id":       ObjectId(),
                "custId":    cust["_id"],
                "status":    status,
                "items":     items,
                "amount":    amount,
                "createdAt": created,
            }
            if status in ("shipped", "completed"):
                doc["shippedAt"] = created + timedelta(days=random.randint(1, 5))
            orders.append(doc)

    db.orders.insert_many( )
    print(f"\r  ✅  {len(orders)} orders inserted")


def seed_inventory(db) -> None:
    """
    Seed 10 inventory records — one per SKU.
    sku 'A1' intentionally has qty=2 so the transaction demo can
    demonstrate an "Insufficient stock" abort when qty:3 is ordered.
    """
    print("\n[3/5] Seeding inventory …")
    db.inventory.drop()

    docs = []
    for p in PRODUCTS:
        # A1 intentionally low — used for the transaction failure demo
        qty = 2 if p["sku"] == "A1" else random.randint(20, 200)
        docs.append({
            "sku":       p["sku"],
            "name":      p["name"],
            "unitPrice": p["unitPrice"],
            "qty":       qty,
        })

    db.inventory.insert_many(docs)
    print(f"\r  ✅  {len(docs)} inventory records inserted  "
          f"(A1 qty=2 — ready for transaction failure demo)")


def seed_audit_log(db) -> None:
    """Create the audit_log collection (empty — written live in Demo 6)."""
    print("\n[4/5] Creating audit_log collection (empty) …")
    db.audit_log.drop()
    # Insert + delete a placeholder to force collection creation
    result = db.audit_log.insert_one({"_placeholder": True})
    db.audit_log.delete_one({"_id": result.inserted_id})
    print("  ✅  audit_log collection ready")


def seed_orders_large(db, customers: list, total: int = 500_000) -> None:
    """
    Seed `total` lean order docs for the Index Before/After demo (Demo 4).
    Documents are intentionally small (no embedded items) so inserts are fast.
    NO index is created — the demo shows COLLSCAN first, then IXSCAN after.
    """
    print(f"\n[5/5] Seeding orders_large ({total:,} docs for index demo) …")
    print("  This takes ~2-3 minutes. Use --skip-large to omit during dry-runs.")
    db.orders_large.drop()

    cust_ids   = [c["_id"] for c in customers]
    batch_size = 5_000
    inserted   = 0
    t0         = time.time()

    while inserted < total:
        n = min(batch_size, total - inserted)
        batch = []
        for _ in range(n):
            created = rand_date(730)
            batch.append({
                "custId":    random.choice(cust_ids),
                "status":    random.choice(STATUSES),
                "amount":    round(random.uniform(10, 800), 2),
                "createdAt": created,
            })
        db.orders_large.insert_many(batch, ordered=False)
        inserted += n
        progress("orders_large", inserted, total)

    elapsed = time.time() - t0
    print(f"\n  ✅  {inserted:,} docs inserted in {elapsed:.1f}s")
    print("  ⚠️   NO index created — run explain() first to show COLLSCAN")


# ══════════════════════════════════════════════════════════════════════════════
# CHEAT SHEET (printed after seeding)
# ══════════════════════════════════════════════════════════════════════════════

def print_cheat_sheet(db_name: str) -> None:
    alice_id  = str(HERO_IDS["alice"])
    bob_id    = str(HERO_IDS["bob"])
    carol_id  = str(HERO_IDS["carol"])
    david_id  = str(HERO_IDS["david"])
    ord_a3_id = "665f000000000000000002a3"   # Alice's pending order
    ord_b1_id = "665f000000000000000002b1"   # Bob's completed order

    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              DEMO CHEAT SHEET  —  use '{db_name}' database                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

HERO CUSTOMER IDs (copy-paste into Compass / mongosh)
  Alice Chen  (APAC · gold)   → ObjectId("{alice_id}")
  Bob Patel   (EMEA · silver) → ObjectId("{bob_id}")
  Carol Smith (AMER · gold)   → ObjectId("{carol_id}")
  David Kim   (APAC · bronze) → ObjectId("{david_id}")

──────────────────────────────────────────────────────────────────────────────
DEMO 1 — verify the dataset
──────────────────────────────────────────────────────────────────────────────
  db.customers.countDocuments()            // → 60
  db.orders.countDocuments()               // → ~300+
  db.orders.findOne()                      // show embedded items
  db.customers.find({{ tier:"gold" }})

──────────────────────────────────────────────────────────────────────────────
DEMO 2 — CRUD
──────────────────────────────────────────────────────────────────────────────
  // READ: completed orders over $100
  db.orders.find(
    {{ status:"completed", amount:{{ $gt:100 }} }},
    {{ _id:0, custId:1, amount:1, status:1 }}
  )

  // READ: orders containing item sku "A1"  (replaces a SQL JOIN)
  db.orders.find({{ "items.sku": "A1" }})

  // UPDATE: mark Alice's pending order as shipped
  db.orders.updateOne(
    {{ _id: ObjectId("{ord_a3_id}") }},
    {{ $set: {{ status:"shipped", shippedAt: new Date() }} }}
  )

  // UPDATE: add tracking to the A1 line-item using positional $
  db.orders.updateOne(
    {{ _id: ObjectId("{ord_a3_id}"), "items.sku":"A1" }},
    {{ $set: {{ "items.$.tracking": "TRK-99021" }} }}
  )

  // DELETE: pending orders older than 30 days
  db.orders.deleteMany({{
    status:"pending",
    createdAt:{{ $lt: new Date(Date.now() - 30*24*60*60*1000) }}
  }})

──────────────────────────────────────────────────────────────────────────────
DEMO 3 — Aggregation (SQL → MongoDB)
──────────────────────────────────────────────────────────────────────────────
  db.orders.aggregate([
    {{ $match:   {{ status: "completed" }} }},
    {{ $lookup:  {{ from:"customers", localField:"custId",
                   foreignField:"_id", as:"customer" }} }},
    {{ $unwind:  "$customer" }},
    {{ $group:   {{ _id:"$customer.region",
                   totalRevenue:{{ $sum:"$amount" }},
                   orderCount:{{ $sum:1 }},
                   avgOrder:{{ $avg:"$amount" }},
                   tiers:{{ $addToSet:"$customer.tier" }} }} }},
    {{ $project: {{ _id:0, region:"$_id", totalRevenue:1,
                   orderCount:1, avgOrder:{{ $round:["$avgOrder",2] }}, tiers:1 }} }},
    {{ $sort:    {{ totalRevenue: -1 }} }}
  ])

──────────────────────────────────────────────────────────────────────────────
DEMO 4 — Index Before & After  (uses orders_large — 500K docs)
──────────────────────────────────────────────────────────────────────────────
  // Step 1: Check indexes
  db.orders_large.getIndexes()             // → only _id

  // Step 2: BEFORE index — should show COLLSCAN
  db.orders_large.explain("executionStats")
    .find({{ custId: ObjectId("{alice_id}"), status:"completed" }})
  // Look for:  stage:"COLLSCAN", totalDocsExamined:500000

  // Step 3: Create compound index
  db.orders_large.createIndex(
    {{ custId: 1, status: 1 }},
    {{ name: "idx_custId_status" }}
  )

  // Step 4: AFTER index — should show IXSCAN
  db.orders_large.explain("executionStats")
    .find({{ custId: ObjectId("{alice_id}"), status:"completed" }})
  // Look for:  stage:"IXSCAN", totalDocsExamined<<500000

  // Bonus: TTL index on pending orders (expire after 7 days)
  db.orders_large.createIndex(
    {{ createdAt: 1 }},
    {{ expireAfterSeconds: 604800,
       partialFilterExpression: {{ status:"pending" }} }}
  )

──────────────────────────────────────────────────────────────────────────────
DEMO 5 — Node.js  (run via node or show in Compass)
──────────────────────────────────────────────────────────────────────────────
  // Upsert — insert if missing, update if present
  db.customers.updateOne(
    {{ email: "eve@example.com" }},
    {{ $set: {{ name:"Eve Adams", region:"AMER", tier:"silver" }},
      $setOnInsert: {{ createdAt: new Date() }} }},
    {{ upsert: true }}
  )

──────────────────────────────────────────────────────────────────────────────
DEMO 6 — Transactions  (inventory sku "A1" has qty=2)
──────────────────────────────────────────────────────────────────────────────
  // Verify stock before demo
  db.inventory.findOne({{ sku:"A1" }})    // → qty: 2

  // In Node.js placeOrder() — try qty:3 first (will abort), then qty:1
  // After abort:
  db.inventory.findOne({{ sku:"A1" }})    // → still qty: 2  ✅
  db.audit_log.countDocuments()           // → 0

  // After commit:
  db.inventory.findOne({{ sku:"A1" }})    // → qty: 1
  db.audit_log.find()                     // → 1 audit record
""")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed MongoDB demo data for MongoDB for Relational Developers presentation"
    )
    parser.add_argument(
        "--uri", default="mongodb://localhost:27017",
        help="MongoDB connection string (default: mongodb://localhost:27017)"
    )
    parser.add_argument(
        "--db", default="shop",
        help="Database name (default: shop — matches demo slides)"
    )
    parser.add_argument(
        "--skip-large", action="store_true",
        help="Skip the 500K orders_large collection (faster dry-run)"
    )
    parser.add_argument(
        "--drop", action="store_true",
        help="Drop the entire database before seeding"
    )
    args = parser.parse_args()

    print("━" * 70)
    print("  MongoDB for Relational Developers — Demo Data Seeder")
    print("━" * 70)
    print(f"  URI : {args.uri}")
    print(f"  DB  : {args.db}")
    print(f"  500K: {'skipped (--skip-large)' if args.skip_large else 'will seed'}")
    print("━" * 70)

    # ── Connect ───────────────────────────────────────────────────────────────
    try:
        client = MongoClient(args.uri, serverSelectionTimeoutMS=5_000)
        client.admin.command("ping")
        print(f"\n  ✅  Connected to MongoDB")
    except Exception as e:
        print(f"\n  ❌  Cannot connect: {e}", file=sys.stderr)
        sys.exit(1)

    db = client[args.db]

    if args.drop:
        print(f"\n  ⚠️   Dropping database '{args.db}' …")
        client.drop_database(args.db)

    # ── Seed ─────────────────────────────────────────────────────────────────
    t_start = time.time()

    customers = seed_customers(db)
    seed_orders(db, customers)
    seed_inventory(db)
    seed_audit_log(db)

    if not args.skip_large:
        seed_orders_large(db, customers)
    else:
        print("\n[5/5] Skipped orders_large (--skip-large flag set)")

    elapsed = time.time() - t_start

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "━" * 70)
    print(f"  ✅  Seeding complete in {elapsed:.1f}s")
    print("━" * 70)
    print(f"\n  Collections in '{args.db}':")
    for name in sorted(db.list_collection_names()):
        count = db[name].estimated_document_count()
        print(f"    {name:<20} {count:>10,} docs")

    print_cheat_sheet(args.db)
    client.close()


if __name__ == "__main__":
    main()
