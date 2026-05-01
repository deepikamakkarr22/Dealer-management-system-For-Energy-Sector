"""
Vibe Agent for IOCL DMS — powered by Groq + Llama 3.3 70B (free tier).

Agentic tool-use loop:
  1. Receives plain-English business requirement
  2. Calls MongoDB tools (list_collections, get_schema, aggregate, etc.)
     via Groq's OpenAI-compatible function-calling API
  3. Returns structured result: data + MongoDB query + explanation
     + what Oracle APEX would require
"""
import json
import os
from groq import Groq
from app.services.mongo_tools import TOOL_DEFINITIONS_GROQ, TOOL_REGISTRY

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


SYSTEM_PROMPT = """You are an expert MongoDB developer and data analyst embedded inside the IOCL (Indian Oil Corporation Ltd) Dealer Management System.

You have access to a live MongoDB database called iocl_dms with these collections:
- dealers: Petrol/diesel/LPG dealers across India with KPIs, credit limits, locations
- inventory: Fuel stock levels per dealer per product (MS, HSD, SKO, LPG14, LPG19, XP95)
- orders: Supply indents from dealers — full order lifecycle
- complaints: Dealer grievances with category, priority, resolution
- users: System users (ignore for business queries)

Your job:
1. Understand the plain-English business requirement
2. Use the MongoDB tools to inspect schema and run the right queries
3. Return results in the exact JSON format below

ALWAYS follow this sequence:
- Call list_collections first if unsure what data exists
- Call get_schema before writing any query on a collection
- Use aggregate for grouping, ranking, or multi-field analysis
- Use update_documents to demonstrate schema flexibility
- Use find_documents for simple filtered lookups

RESPONSE FORMAT — return ONLY a valid JSON object with exactly these keys:
{
  "title": "Short title for what was built",
  "summary": "2-3 sentence explanation of the insight",
  "mongodb_query": {
    "tool": "aggregate | find_documents | update_documents",
    "collection": "collection name",
    "pipeline_or_filter": <exact pipeline array or filter object used>
  },
  "results": <actual data returned from MongoDB — array of objects>,
  "result_type": "table | update_confirmation",
  "columns": ["col1", "col2"],
  "mongodb_advantage": "Why MongoDB handles this natively",
  "oracle_apex_equivalent": "What Oracle APEX would require — be specific about PL/SQL, DDL, licenses, steps"
}

Return ONLY the JSON object. No markdown, no explanation outside the JSON."""


DEMO_SCENARIOS = [
    {
        "id": "credit_risk",
        "label": "Credit Risk Dealers",
        "icon": "bi-exclamation-triangle-fill text-danger",
        "prompt": "Show me all dealers whose outstanding balance exceeds 85% of their credit limit, ranked worst first. Include their name, state, credit limit, outstanding amount and utilisation percentage.",
    },
    {
        "id": "ev_charging",
        "label": "Add EV Charging Field",
        "icon": "bi-ev-station-fill text-success",
        "prompt": "Add an EV charging capability field to petrol & diesel dealers. Set ev_charging_available to true for some of them. Then show me a count of how many dealers have EV charging by state.",
    },
    {
        "id": "territory_performance",
        "label": "Territory Performance",
        "icon": "bi-bar-chart-fill text-primary",
        "prompt": "Show territory performance scorecard — for each state calculate average compliance score, average customer rating, total dealers, and total outstanding balance. Rank by compliance score worst first.",
    },
]


def run_vibe_agent(prompt: str) -> dict:
    """
    Run Groq + Llama agent with MongoDB tool-use loop.
    Returns structured dict with results, query, and comparison.
    """
    client = _get_client()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": prompt},
    ]

    tool_calls_log = []
    max_iterations = 8

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOL_DEFINITIONS_GROQ,
            tool_choice="auto",
            max_tokens=4096,
            temperature=0.1,
        )

        choice  = response.choices[0]
        message = choice.message

        # Append assistant turn to history
        messages.append({
            "role":       "assistant",
            "content":    message.content or "",
            "tool_calls": [
                {
                    "id":       tc.id,
                    "type":     "function",
                    "function": {
                        "name":      tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in (message.tool_calls or [])
            ] or None,
        })

        # ── Agent done — parse final JSON response ────────────────────
        if choice.finish_reason == "stop":
            text = message.content or ""
            try:
                start  = text.find("{")
                end    = text.rfind("}") + 1
                result = json.loads(text[start:end])
                result["tool_calls_log"] = tool_calls_log
                return result
            except Exception:
                return {
                    "title":                "Response",
                    "summary":              text,
                    "mongodb_query":        {},
                    "results":              [],
                    "result_type":          "table",
                    "columns":              [],
                    "mongodb_advantage":    "",
                    "oracle_apex_equivalent": "",
                    "tool_calls_log":       tool_calls_log,
                }

        # ── Tool calls — execute and feed results back ─────────────────
        if choice.finish_reason == "tool_calls" and message.tool_calls:
            for tc in message.tool_calls:
                tool_name = tc.function.name
                try:
                    tool_input = json.loads(tc.function.arguments)
                except Exception:
                    tool_input = {}

                tool_calls_log.append({"tool": tool_name, "input": tool_input})

                if tool_name in TOOL_REGISTRY:
                    try:
                        result = TOOL_REGISTRY[tool_name](**tool_input)
                    except Exception as e:
                        result = {"error": str(e)}
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                messages.append({
                    "role":         "tool",
                    "tool_call_id": tc.id,
                    "content":      json.dumps(result),
                })

    return {
        "title":                "Timeout",
        "summary":              "Agent reached maximum iterations.",
        "results":              [],
        "result_type":          "table",
        "columns":              [],
        "mongodb_advantage":    "",
        "oracle_apex_equivalent": "",
        "tool_calls_log":       tool_calls_log,
    }
