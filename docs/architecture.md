# IOCL Dealer Management System — Architecture

## What is a Dealer Management System?

A **Dealer Management System (DMS)** is an integrated software platform that enables oil marketing companies like IOCL to manage their entire dealer network end-to-end — from onboarding and licensing through daily inventory replenishment, order processing, sales analytics, and complaint resolution.

---

## Challenges with Any DMS

| Challenge | Description |
|-----------|-------------|
| **Scale & Heterogeneity** | IOCL has 50,000+ petrol stations across India — each with different products, capacities, and compliance requirements |
| **Real-time Inventory** | Fuel stock changes every hour; stale data causes supply gaps or overstocking |
| **Schema Flexibility** | Dealers sell different product mixes (MS/HSD/LPG/Lubes); a rigid relational schema is painful to evolve |
| **Geographically Distributed** | Dealers across 29 states, multiple regional offices, varied network connectivity |
| **Compliance Tracking** | License renewals, price board audits, equipment calibration — all need structured audit trails |
| **High Write Throughput** | Hundreds of simultaneous indent (order) submissions from dealers nationwide |
| **Complex Reporting** | Multi-dimensional analytics: state × product × time × dealer tier |
| **Credit Risk** | Real-time outstanding balance tracking against credit limits prevents bad debt |

---

## Why MongoDB for IOCL DMS?

### 1. Flexible Document Model
Each dealer document embeds contact, KPIs, and license data in one read — no costly JOINs across 10 relational tables.

```json
{
  "dealer_code": "IOCL-UP-0042",
  "name": "Sharma Fuel Centre",
  "contact": { "city": "Lucknow", "state": "Uttar Pradesh" },
  "product_type": "Petrol & Diesel",
  "kpis": { "monthly_volume_kl": 320, "customer_rating": 4.2 },
  "outstanding_balance": 125000
}
```

### 2. Embedded Arrays for Order Line Items
Order items are stored as an embedded array — a single document holds the full indent, making retrieval and audit trivial.

### 3. Aggregation Pipeline for Analytics
MongoDB's `$group`, `$lookup`, `$project` pipeline replaces complex SQL GROUP BY + JOIN queries for sales/compliance reports.

### 4. Horizontal Scalability
Sharding by `contact.state` or `dealer_code` distributes load across regional data centres.

### 5. Change Streams
Real-time triggers on inventory collection can fire automated low-stock alerts to the supply chain team.

### 6. Atlas Search
Full-text search over dealer names, addresses, and complaint descriptions without a separate search engine.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│   Browser  ──  Flask Jinja2 Templates  ──  Bootstrap 5 + Chart.js│
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP / REST
┌────────────────────────────▼────────────────────────────────────┐
│                     APPLICATION LAYER (Flask)                   │
│                                                                 │
│  /auth      /dashboard   /dealers   /inventory                  │
│  /orders    /sales       /complaints  /reports                  │
│                                                                 │
│  Flask-Login (session)  │  Flask-PyMongo (ODM)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │ PyMongo Driver
┌────────────────────────────▼────────────────────────────────────┐
│                       DATA LAYER (MongoDB)                      │
│                                                                 │
│   Collection        Purpose                 Key Indexes         │
│   ──────────────    ────────────────────    ──────────────────  │
│   users             Auth & roles            username (unique)   │
│   dealers           Dealer master data      dealer_code, state  │
│   inventory         Stock per dealer-prod   dealer_id+product   │
│   orders            Indents & dispatch      order_no, dealer    │
│   complaints        Grievance tracking      dealer_code, status │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow — Order Lifecycle

```
Dealer Portal          IOCL Backend          MongoDB
     │                      │                    │
     │── Submit Indent ─────►│                    │
     │                      │── Insert order ───►│ orders (Pending)
     │                      │── Check credit ───►│ dealers
     │                      │                    │
     │                      │── Approve order ──►│ orders (Approved)
     │                      │                    │
     │                      │── Dispatch ───────►│ orders (Dispatched)
     │                      │── Deduct stock ───►│ inventory
     │                      │                    │
     │◄─ Delivery confirm ──│── Mark Delivered ─►│ orders (Delivered)
     │                      │── Update balance ─►│ dealers.outstanding
```

---

## MongoDB Collection Schemas

### dealers
```
dealer_code     String   unique
name            String
owner_name      String
contact         Object   { phone, email, address, city, state, pincode }
product_type    String   enum: Petrol & Diesel | LPG | Lubricants | Multi
license_no      String
license_expiry  Date
credit_limit    Number
outstanding_bal Number
kpis            Object   { monthly_volume_kl, customer_rating, compliance_score }
status          String   enum: Active | Inactive | Suspended
```

### orders
```
order_no        String   unique  e.g. ORD-2024-000123
dealer_code     String   ref → dealers
items           Array    [{ product_code, qty, unit, rate, amount }]
total_amount    Number
status          String   Pending → Approved → Dispatched → Delivered
payment_mode    String   Credit | Cash | DD | NEFT
payment_status  String   Paid | Unpaid | Partial
dispatch_date   Date
vehicle_no      String
```

### inventory
```
dealer_code     String
product_code    String   MS | HSD | SKO | LPG14 | LPG19 | XP95
current_stock   Number
tank_capacity   Number
reorder_level   Number
last_receipt    Date
```

### complaints
```
ref_no          String   unique
dealer_code     String
category        String   Fuel Quality | Supply Delay | Billing | ...
subject         String
priority        String   High | Medium | Low
status          String   Open | In Progress | Resolved | Closed
assigned_to     String
resolution      String
```

---

## Key Aggregation Queries

### Monthly Revenue Trend
```javascript
db.orders.aggregate([
  { $match: { status: { $in: ["Delivered","Dispatched"] } } },
  { $group: {
      _id: { year: { $year: "$created_at" }, month: { $month: "$created_at" } },
      total: { $sum: "$total_amount" }
  }},
  { $sort: { "_id.year": 1, "_id.month": 1 } }
])
```

### Low Stock Dealers
```javascript
db.inventory.find({
  $expr: { $lte: ["$current_stock", "$reorder_level"] }
})
```

### State-wise Compliance
```javascript
db.dealers.aggregate([
  { $group: {
      _id: "$contact.state",
      avg_compliance: { $avg: "$kpis.compliance_score" },
      dealer_count:   { $sum: 1 }
  }},
  { $sort: { avg_compliance: -1 } }
])
```
