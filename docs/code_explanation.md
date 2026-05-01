# Code Explanation — vibe_agent.py & mongo_tools.py

## Overview

These two files together power the **Vibe Coding** feature of the IOCL DMS.
They form the AI + database intelligence layer that sits between a plain-English
prompt typed by a user and the live MongoDB data returned to the screen.

```
User types prompt
      ↓
vibe_agent.py   ← interprets the prompt, orchestrates the conversation with GPT-4o
      ↓
mongo_tools.py  ← executes the actual MongoDB operations, returns real data
      ↓
Live result shown in browser
```

---

## File 1 — `app/services/mongo_tools.py`

### What it is

A set of **Python functions that act as MongoDB MCP tools**. Each function
performs one type of database operation — listing collections, inspecting schemas,
querying, aggregating, updating — and returns a JSON-safe result.

These functions mirror what the official `@mongodb-js/mongodb-mcp-server` (Node.js)
exposes over the MCP protocol, but implemented directly in Python so no Node.js
subprocess is needed.

The AI agent calls these functions when it needs to talk to the database.

---

### Functions

#### `_serialise(obj)`

**What it does:** Converts MongoDB documents into plain Python dicts that can
be turned into JSON.

MongoDB returns documents with special types that Python's `json` module cannot
handle directly — `ObjectId` (the MongoDB `_id` field) and `datetime`. This
function recursively walks through any nested structure and converts:
- `ObjectId` → plain string (`"64a3f2..."`)
- `datetime` → ISO string (`"2024-05-01T10:30:00"`)
- dicts and lists → recursively processed

Every tool function calls `_serialise` before returning data so the result is
always safe to pass to `json.dumps()`.

---

#### `list_collections()`

**What it does:** Returns the names of all collections in the `iocl_dms`
database along with how many documents are in each one.

**When the agent calls it:** At the very start of any query when it needs to
understand what data exists. The system prompt instructs the agent to always
call this first when it is unsure.

**Example output:**
```json
{
  "collections": [
    { "collection": "complaints", "document_count": 80 },
    { "collection": "dealers",    "document_count": 60 },
    { "collection": "inventory",  "document_count": 240 },
    { "collection": "orders",     "document_count": 400 }
  ]
}
```

---

#### `get_schema(collection, sample_size=3)`

**What it does:** Samples a few real documents from a collection and reports
what fields exist, what type each field is, and an example value.

**Why this matters:** The agent does not know in advance that the `dealers`
collection has a field called `outstanding_balance` or that `kpis` is a nested
object. Before writing any query, the agent calls `get_schema` to learn the
exact field names so it does not guess and get them wrong.

**Example output for `dealers`:**
```json
{
  "collection": "dealers",
  "fields": [
    { "name": "dealer_code",          "type": "str",   "example": "IOCL-MH-0012" },
    { "name": "name",                 "type": "str",   "example": "Sharma Fuel Centre" },
    { "name": "credit_limit",         "type": "float", "example": 2500000.0 },
    { "name": "outstanding_balance",  "type": "float", "example": 1850000.0 },
    { "name": "contact",              "type": "dict",  "example": "<dict>" },
    { "name": "kpis",                 "type": "dict",  "example": "<dict>" }
  ],
  "sample_documents": [ ... ]
}
```

---

#### `find_documents(collection, filter, projection, limit, sort_field, sort_order)`

**What it does:** Fetches documents from a collection matching an optional
filter. Supports projection (choose which fields to return), sorting, and
a limit (capped at 50 for demo safety).

**When the agent calls it:** For straightforward lookups — "show me dealers
in Maharashtra" or "find all cancelled orders".

**Example call by the agent:**
```json
{
  "collection": "orders",
  "filter": { "status": "Pending" },
  "sort_field": "created_at",
  "sort_order": -1,
  "limit": 20
}
```

---

#### `aggregate(collection, pipeline)`

**What it does:** Runs a full MongoDB aggregation pipeline against a collection
and returns the results. This is the most powerful tool — it handles grouping,
calculations, joins between collections (`$lookup`), ranking, and
multi-dimensional analytics.

**Special behaviour:** MongoDB's `$group` stage stores the group key in a field
called `_id`. The frontend cannot display a column called `_id` meaningfully,
so this function **renames `_id` automatically**:
- If `_id` is a simple value (e.g. a state name like `"Maharashtra"`) → renamed to `group_by`
- If `_id` is a compound object (e.g. `{"year": 2024, "month": 5}`) → its fields are
  flattened directly into the result document

This means the frontend always receives clean, displayable column names.

**Example — territory performance pipeline the agent might build:**
```json
[
  { "$group": {
      "_id": "$contact.state",
      "avg_compliance": { "$avg": "$kpis.compliance_score" },
      "avg_rating":     { "$avg": "$kpis.customer_rating" },
      "total_dealers":  { "$sum": 1 }
  }},
  { "$sort": { "avg_compliance": 1 } }
]
```

**After `_id` renaming, one result row looks like:**
```json
{ "group_by": "Bihar", "avg_compliance": 48.2, "avg_rating": 3.1, "total_dealers": 4 }
```

---

#### `update_documents(collection, filter, update, many=True)`

**What it does:** Adds new fields or updates existing fields on matching
documents. Restricted to `$set` operations only (no deletions or replacements)
for demo safety.

**Why this is the key demo moment:** This function proves MongoDB's schema
flexibility live. When you add a field like `ev_charging_available: true`
to a subset of dealers, MongoDB accepts it instantly — no ALTER TABLE,
no DBA, no downtime. Documents that do not have the field simply do not
have it; documents that do have it carry it. Both coexist in the same collection.

**Example call:**
```json
{
  "collection": "dealers",
  "filter": { "product_type": "Petrol & Diesel" },
  "update": { "$set": { "ev_charging_available": true } }
}
```

**Output:**
```json
{ "matched_count": 28, "modified_count": 28 }
```

---

#### `count_documents(collection, filter)`

**What it does:** Returns the count of documents matching an optional filter.
Used for simple "how many" questions.

**Example call for "how many orders are pending approval":**
```json
{
  "collection": "orders",
  "filter": { "status": "Pending" }
}
```

**Output:**
```json
{ "collection": "orders", "filter": { "status": "Pending" }, "count": 47 }
```

---

### Tool Registry and Tool Definitions

At the bottom of `mongo_tools.py` there are two important data structures:

**`TOOL_REGISTRY`** — a plain Python dict that maps each tool name (a string)
to its function:
```python
TOOL_REGISTRY = {
    "list_collections": list_collections,
    "get_schema":       get_schema,
    "find_documents":   find_documents,
    "aggregate":        aggregate,
    "update_documents": update_documents,
    "count_documents":  count_documents,
}
```
When the agent says "call `aggregate` with these arguments", the agent loop
looks up `TOOL_REGISTRY["aggregate"]` and calls the function with those arguments.

**`TOOL_DEFINITIONS`** — a list of JSON schemas describing each tool to the
AI agent. This is how the agent knows what tools exist, what arguments each
tool accepts, and what each tool does. Written in Anthropic format.

**`TOOL_DEFINITIONS_GROQ`** — the same definitions converted to OpenAI/Groq
function-calling format (the `parameters` key instead of `input_schema`).
GPT-4o reads this list to decide which tool to call and with what arguments.

The conversion is done by `_to_groq()` which simply renames the schema key
and wraps each tool in `{ "type": "function", "function": {...} }`.

---

---

## File 2 — `app/services/vibe_agent.py`

### What it is

The **AI agent orchestrator**. It receives a plain-English prompt, runs a
multi-turn conversation with GPT-4o where the model is allowed to call
MongoDB tools, and returns a structured result containing the data, the
query that was used, and a comparison with what Oracle APEX would require.

---

### Key Components

#### `_get_client()` — lazy OpenAI client

Creates the OpenAI SDK client on first use using the `OPENAI_API_KEY`
environment variable. Uses a module-level `_client` variable so the
connection is created once and reused across requests.

---

#### `SYSTEM_PROMPT`

A detailed instruction block sent to GPT-4o at the start of every conversation.
It tells the model:

1. **Who it is** — a MongoDB expert embedded in the IOCL DMS
2. **What data exists** — the five collections and what each contains
3. **What sequence to follow** — always call `list_collections` first,
   then `get_schema`, then the appropriate query tool
4. **What format to return** — a strict JSON object with exactly these keys:
   `title`, `summary`, `mongodb_query`, `results`, `result_type`, `columns`,
   `mongodb_advantage`, `oracle_apex_equivalent`

The format instruction is critical. Without it the model would return a
narrative explanation. With it, every response can be parsed and rendered
directly into the results panel.

---

#### `DEMO_SCENARIOS`

A list of three pre-built demo prompts that appear as one-click buttons
in the Vibe Coding panel:

| Scenario | What it demonstrates |
|----------|---------------------|
| Credit Risk Dealers | Aggregation pipeline with `$project` + `$match` + `$sort` |
| Add EV Charging Field | Schema flexibility — `update_documents` adds a new field instantly |
| Territory Performance | Multi-field `$group` analytics across all dealers by state |

---

#### `_extract_json(text)` — robust JSON parser

GPT-4o does not always return a clean JSON string. Sometimes it wraps the
output in markdown code fences like this:

````
```json
{ "title": "...", "results": [...] }
```
````

A simple `json.loads(text)` would fail on this. `_extract_json` handles
three cases:

1. **Markdown fenced block** — uses a regex to find and extract the content
   between ` ```json ``` ` tags
2. **Plain JSON with surrounding text** — finds the first `{` and last `}`
   and parses just that slice
3. **Nothing found** — raises `ValueError` which the caller catches and
   handles gracefully

---

#### `_normalise_results(results)` — type safety for the frontend

The frontend JavaScript always expects `results` to be a list of objects
so it can build a table. But GPT-4o might put different types in this field
depending on what the tools returned:

| GPT-4o returns | `_normalise_results` converts to |
|----------------|----------------------------------|
| A list (normal) | Returned as-is |
| A single dict | Wrapped in a list: `[dict]` |
| A number (e.g. a count) | `[{"value": N}]` |
| Anything else | Empty list `[]` |

---

#### `run_vibe_agent(prompt)` — the main agentic loop

This is the core function. It runs a **multi-turn conversation** between
the user's prompt and GPT-4o, allowing the model to call MongoDB tools
as many times as needed before producing a final answer.

**Step-by-step walkthrough:**

```
Step 1 — Build initial messages
    messages = [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user",   content: <user's prompt> }
    ]

Step 2 — Call GPT-4o with tool definitions
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOL_DEFINITIONS_GROQ,   ← GPT-4o can see all 6 tools
        tool_choice="auto"             ← model decides when to call tools
    )

Step 3a — If GPT-4o calls a tool (finish_reason == "tool_calls"):
    - Read the tool name and arguments from response
    - Look up the function in TOOL_REGISTRY
    - Call the Python function with those arguments
    - MongoDB executes the query
    - Append the result back to messages as a "tool" role message
    - Loop back to Step 2 (GPT-4o sees the tool result and continues)

Step 3b — If GPT-4o is done (finish_reason == "stop"):
    - Extract the JSON from the response text using _extract_json()
    - Normalise results using _normalise_results()
    - Attach the tool_calls_log (what tools were called)
    - Return the final structured dict to Flask
```

**Why `tool_calls` is conditionally included in assistant messages:**

When GPT-4o makes tool calls, the OpenAI API requires the assistant message
to include the `tool_calls` array. But when GPT-4o is just thinking (no tool
call), the message must NOT include `tool_calls` at all — the API rejects
`tool_calls: null`. The code handles this with an explicit `if message.tool_calls`
check before adding the key.

**`max_iterations = 10`** — safety limit to prevent infinite loops if the
model keeps calling tools without finishing. In practice most queries resolve
in 2–4 iterations.

---

### Complete Example — "How many orders are in pending status?"

```
Iteration 1:
  User prompt → GPT-4o
  GPT-4o decides → call list_collections()
  Result: [dealers(60), inventory(240), orders(400), complaints(80)]

Iteration 2:
  Tool result appended → GPT-4o
  GPT-4o decides → call count_documents("orders", {"status": "Pending"})
  Result: { collection: "orders", filter: {status:"Pending"}, count: 47 }

Iteration 3:
  Tool result appended → GPT-4o
  GPT-4o finish_reason = "stop"
  GPT-4o returns JSON:
  {
    "title": "Pending Orders Count",
    "summary": "There are 47 orders currently in Pending status...",
    "mongodb_query": { "tool": "count_documents", ... },
    "results": [{ "count": 47 }],
    "result_type": "metric",
    "columns": ["count"],
    "mongodb_advantage": "...",
    "oracle_apex_equivalent": "..."
  }

_extract_json() parses this → _normalise_results() confirms it's a list
→ returned to Flask → rendered in the browser
```

---

### How the Two Files Connect

```
vibe_agent.py                          mongo_tools.py
─────────────────────────────────────────────────────────
run_vibe_agent(prompt)
  │
  ├─ Sends TOOL_DEFINITIONS_GROQ ──── built from TOOL_DEFINITIONS
  │   to GPT-4o so it knows what      with _to_groq() conversion
  │   tools are available
  │
  ├─ GPT-4o responds: "call aggregate(dealers, [...])"
  │
  ├─ Looks up TOOL_REGISTRY["aggregate"] ──── returns aggregate()
  │
  ├─ Calls aggregate(collection, pipeline)
  │     │
  │     ├─ PyMongo executes against MongoDB
  │     ├─ _serialise() cleans ObjectId/datetime
  │     ├─ _id renamed to group_by
  │     └─ Returns { results: [...] }
  │
  ├─ Appends result to messages
  ├─ Loops back → GPT-4o reads result → decides what to do next
  │
  └─ When done → _extract_json() + _normalise_results() → return
```

---

### Files Summary

| File | Role | Key exports |
|------|------|-------------|
| `mongo_tools.py` | Database layer — executes MongoDB operations | `TOOL_REGISTRY`, `TOOL_DEFINITIONS_GROQ` |
| `vibe_agent.py` | AI layer — orchestrates GPT-4o + tool calls | `run_vibe_agent()`, `DEMO_SCENARIOS` |
