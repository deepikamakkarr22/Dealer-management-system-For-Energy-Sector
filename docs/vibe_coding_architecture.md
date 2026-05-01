# Vibe Coding Architecture — IOCL SDMS
## AI Agent + MongoDB + Groq (Llama 3.3 70B)

---

## Overview

Vibe Coding is an AI-powered feature embedded inside the IOCL Dealer Management System.
A user describes a business requirement in plain English. The AI Agent interprets it,
queries the live MongoDB database using MCP-equivalent tools, and renders the result
— no SQL, no PL/SQL, no DBA involved.

---

## Full Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        BROWSER (User)                            │
│                                                                  │
│   "Show dealers with credit risk above 85%"  [Generate]          │
│                                                                  │
│   ┌─────────────────┐      ┌──────────────────────────────────┐  │
│   │  Live Results   │      │  MongoDB Query (transparent)     │  │
│   │  (real data)    │      │  pipeline shown to audience      │  │
│   └─────────────────┘      └──────────────────────────────────┘  │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │  MCP Tool Call Log  (what the agent did step by step)   │   │
│   └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬──────────────────────────────────────┘
                            │ POST /vibe/generate  { prompt }
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Flask Application Layer                         │
│                  app/routes/vibe.py                              │
│                                                                  │
│   Receives prompt → calls run_vibe_agent(prompt)                 │
└───────────────────────────┬──────────────────────────────────────┘
                            │ Python function call
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│               AI Agent — app/services/vibe_agent.py              │
│                                                                  │
│   Model  : Llama 3.3 70B (via Groq API — free tier)             │
│   SDK    : groq Python SDK                                       │
│   Format : OpenAI-compatible function-calling                    │
│                                                                  │
│   Agentic Loop:                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 1. Receive prompt                                       │   │
│   │ 2. Call Groq API with tool definitions                  │   │
│   │ 3. If finish_reason == "tool_calls":                    │   │
│   │      → Extract tool name + arguments                   │   │
│   │      → Execute MongoDB tool function                   │   │
│   │      → Append result to messages                       │   │
│   │      → Loop back to step 2                             │   │
│   │ 4. If finish_reason == "stop":                         │   │
│   │      → Parse structured JSON response                  │   │
│   │      → Return to Flask                                 │   │
│   └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬──────────────────────────────────────┘
                            │ Groq REST API (HTTPS)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Groq Cloud (Free Tier)                        │
│                                                                  │
│   Model  : llama-3.3-70b-versatile                               │
│   Limit  : 14,400 requests/day, 500K tokens/minute              │
│   Cost   : Free                                                  │
└───────────────────────────┬──────────────────────────────────────┘
                            │ Tool call response back to agent
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│          MongoDB Tool Layer — app/services/mongo_tools.py        │
│                                                                  │
│   Tool               What it does                               │
│   ─────────────────  ────────────────────────────────────────   │
│   list_collections   List all collections + document counts     │
│   get_schema         Sample docs to infer field structure       │
│   find_documents     Filter + sort + project documents          │
│   aggregate          Run full aggregation pipelines             │
│   update_documents   Add/update fields (schema flexibility)     │
│   count_documents    Count matching documents                   │
│                                                                  │
│   All tools return JSON-serialisable results                     │
│   Registry maps tool name → Python function                     │
└───────────────────────────┬──────────────────────────────────────┘
                            │ PyMongo (MongoDB Wire Protocol)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                MongoDB — iocl_dms database                       │
│                                                                  │
│   Collection    Documents   Purpose                              │
│   ───────────   ─────────   ──────────────────────────────────  │
│   dealers       60          Dealer master with KPIs, credit     │
│   inventory     ~240        Fuel stock per dealer per product   │
│   orders        400         Supply indents + lifecycle          │
│   complaints    80          Grievances + resolution             │
│   users         3           System auth (excluded from vibe)    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow — Step by Step

```
Step 1   User types: "Show dealers with credit risk above 85%"
            ↓
Step 2   Flask POST /vibe/generate receives the prompt
            ↓
Step 3   run_vibe_agent() sends prompt + tool definitions to Groq
            ↓
Step 4   Llama 3.3 decides → call list_collections()
         Tool result: dealers, inventory, orders, complaints
            ↓
Step 5   Llama 3.3 decides → call get_schema("dealers")
         Tool result: fields including credit_limit, outstanding_balance
            ↓
Step 6   Llama 3.3 decides → call aggregate("dealers", pipeline)
         Pipeline: $project (utilisation%) → $match (>85%) → $sort
         Tool result: 12 dealers with credit risk
            ↓
Step 7   Llama 3.3 returns structured JSON:
         { title, summary, mongodb_query, results,
           mongodb_advantage, oracle_apex_equivalent }
            ↓
Step 8   Flask returns JSON to browser
            ↓
Step 9   Browser renders:
         - Results table (real dealer data)
         - MongoDB pipeline (transparent, shown to audience)
         - MCP tool call log (list_collections → get_schema → aggregate)
         - MongoDB advantage explanation
         - Oracle APEX comparison
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Bootstrap 5 + Vanilla JS | Vibe coding UI panel |
| Backend | Python 3.9 + Flask 3.0 | Route handling + agent orchestration |
| AI Model | Llama 3.3 70B | Natural language → tool calls |
| AI Platform | Groq API (free tier) | Fast inference, no cost |
| AI SDK | groq Python SDK | OpenAI-compatible function calling |
| Tool Layer | PyMongo (custom MCP-equivalent) | MongoDB operations as callable tools |
| Database | MongoDB 7 | iocl_dms — all SDMS data |

---

## vs Oracle APEX

| Capability | Oracle APEX | This Architecture |
|------------|------------|------------------|
| Business requirement input | Form wizard + APEX builder | Plain English prompt |
| Schema inspection | DBA + SQL Developer | AI Agent → get_schema tool |
| Query generation | PL/SQL developer | Llama 3.3 generates pipeline |
| New field rollout | ALTER TABLE + maintenance window | update_documents → zero downtime |
| Analytics | OBIEE / OAC (licensed) | MongoDB Aggregation Pipeline |
| Real-time | Oracle Streams (licensed) | Change Streams (native) |
| AI integration | Oracle AI Services (licensed) | Groq free tier + open-source model |
| Total extra cost | ₹XX Lakhs/year | ₹0 |

---

## Demo Scenarios

| Scenario | Tools Called | MongoDB Feature Highlighted |
|----------|-------------|----------------------------|
| Credit Risk Dealers | get_schema → aggregate | $project + $match + $sort pipeline |
| Add EV Charging Field | get_schema → update_documents | Schema flexibility — no migration |
| Territory Performance | get_schema → aggregate | Multi-field $group + $sort |

---

## Key Files

```
app/
├── routes/
│   └── vibe.py              Flask blueprint — GET /vibe, POST /vibe/generate
├── services/
│   ├── vibe_agent.py        Groq + Llama agentic loop
│   └── mongo_tools.py       MongoDB MCP-equivalent tool functions
templates/
└── vibe/
    └── panel.html           Vibe coding UI — prompt, results, query, log
```
