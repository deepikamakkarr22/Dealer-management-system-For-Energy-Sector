# IOCL Dealer Management System — Demo

A full-stack demo of an **Indian Oil Corporation Ltd (IOCL) Dealer Management System** built with **Python (Flask)** and **MongoDB**.

---

## What is a Dealer Management System?

A DMS is an integrated platform that lets an oil marketing company manage its dealer network end-to-end:

- **Dealer onboarding & licensing** — register dealers, track license expiry, assign territories
- **Inventory management** — real-time fuel stock levels, reorder alerts, tank capacity tracking
- **Order / indent management** — dealers raise supply indents; the company approves, dispatches, and confirms delivery
- **Sales analytics** — revenue by product, state, dealer tier; trend charts over time
- **Complaint management** — structured grievance tracker with priority, assignment, and resolution
- **Credit management** — real-time outstanding balance vs. credit limit per dealer

---

## Challenges with a DMS at IOCL Scale

| Challenge | Detail |
|-----------|--------|
| Scale | 50,000+ petrol stations across India |
| Schema flexibility | Dealers sell different product mixes — rigid RDBMS schemas are painful |
| Real-time inventory | Fuel stock changes hourly; stale data causes supply gaps |
| High write throughput | Hundreds of simultaneous indent submissions |
| Complex analytics | Multi-dimensional: state × product × time × dealer tier |
| Geographic distribution | 29 states, multiple regional offices, varied connectivity |

---

## Why MongoDB?

| Feature | Benefit for IOCL DMS |
|---------|----------------------|
| **Document model** | Embed contact, KPIs, license in one dealer document — no JOIN overhead |
| **Flexible schema** | Add new product types or KPI fields without migrations |
| **Aggregation pipeline** | Complex analytics with `$group`, `$lookup`, `$project` |
| **Horizontal scaling** | Shard by state or region for geographic distribution |
| **Change streams** | Trigger real-time low-stock alerts |
| **Atlas Search** | Full-text search over dealer names and complaints |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask 3.0 |
| Database | MongoDB 7 (PyMongo + Flask-PyMongo) |
| Auth | Flask-Login + bcrypt |
| Frontend | Jinja2 templates, Bootstrap 5, Chart.js 4 |
| Seed data | Faker (en_IN locale) |

---

## Project Structure

```
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Collection schemas + User model
│   │   ├── user.py
│   │   ├── dealer.py
│   │   ├── inventory.py
│   │   └── order.py
│   └── routes/              # Blueprint-per-module
│       ├── auth.py
│       ├── dashboard.py
│       ├── dealers.py
│       ├── inventory.py
│       ├── orders.py
│       ├── sales.py
│       ├── complaints.py
│       └── reports.py
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── auth/login.html
│   ├── dashboard/home.html
│   ├── dealers/list.html + detail.html
│   ├── inventory/list.html
│   ├── orders/list.html + detail.html
│   ├── sales/overview.html
│   ├── complaints/list.html + detail.html
│   └── reports/home.html
├── static/css/iocl.css      # IOCL brand theme
├── scripts/seed_data.py     # Demo data generator
├── docs/architecture.md     # Architecture deep-dive
├── run.py                   # App entry point
└── requirements.txt
```

---

## Quick Start

### 1. Prerequisites
- Python 3.11+
- MongoDB running locally on port 27017 (or provide `MONGO_URI`)

### 2. Setup

```bash
# Clone / open the project
cd "Dealer management System"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if needed (MONGO_URI, SECRET_KEY)
```

### 3. Seed Demo Data

```bash
python scripts/seed_data.py
```

This creates:
- 3 users (admin / manager / viewer)
- 60 dealers across 15 Indian states
- ~240 inventory records
- 400 orders spanning 12 months
- 80 complaints

### 4. Run the App

```bash
python run.py
```

Open **http://localhost:5000** and log in with:
- Username: `admin`
- Password: `admin123`

---

## Modules

| Module | URL | Description |
|--------|-----|-------------|
| Dashboard | `/dashboard` | KPI cards, sales trend, low-stock alerts |
| Dealers | `/dealers` | Searchable dealer directory with detail view |
| Inventory | `/inventory` | Stock levels with fill-% bars and alert flags |
| Orders | `/orders` | Full order lifecycle with payment tracking |
| Sales | `/sales` | Revenue analytics by product and state |
| Complaints | `/complaints` | Grievance tracker with priority & resolution |
| Reports | `/reports` | 12-month trend, compliance scores |

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full architecture document including:
- System architecture diagram
- Data flow for order lifecycle
- All MongoDB collection schemas
- Key aggregation queries

---

*Demo build — Indian Oil Corporation Ltd. Dealer Management System*
