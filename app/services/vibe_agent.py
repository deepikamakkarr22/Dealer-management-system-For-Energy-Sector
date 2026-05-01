"""
Claude Vibe Agent for IOCL DMS.

Runs an agentic tool-use loop:
  1. Receives a plain-English business requirement
  2. Calls MongoDB MCP tools (list_collections, get_schema, aggregate, etc.)
  3. Returns structured result: data + MongoDB query used + explanation
     + what Oracle APEX would require

Uses claude-sonnet-4-6 with prompt caching on the system prompt.
"""
import json
import os
import anthropic
from app.services.mongo_tools import TOOL_DEFINITIONS, TOOL_REGISTRY

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


SYSTEM_PROMPT = """You are an expert MongoDB developer and data analyst embedded inside the IOCL (Indian Oil Corporation Ltd) Dealer Management System.

You have access to a live MongoDB database called iocl_dms containing these collections:
- dealers: Petrol/diesel/LPG dealers across India with KPIs, credit limits, locations
- inventory: Fuel stock levels per dealer per product (MS, HSD, SKO, LPG14, LPG19, XP95)
- orders: Supply indents from dealers — full order lifecycle
- complaints: Dealer grievances with category, priority, resolution
- users: System users (ignore this for business queries)

Your job:
1. Understand the plain-English business requirement
2. Use the MongoDB tools to inspect the schema and run the right queries
3. Return results in the exact JSON format specified below

ALWAYS follow this sequence:
- Call list_collections first if you're unsure what data exists
- Call get_schema before writing any query on a collection
- Use aggregate for any grouping, ranking, or multi-field analysis
- Use update_documents to demonstrate schema flexibility (adding new fields)
- Use find_documents for simple filtered lookups

RESPONSE FORMAT — you MUST return a JSON object with exactly these keys:
{
  "title": "Short title for what was built",
  "summary": "2-3 sentence explanation of what the query does and what insight it provides",
  "mongodb_query": {
    "tool": "aggregate | find_documents | update_documents",
    "collection": "collection name",
    "pipeline_or_filter": <the exact pipeline array or filter object used>
  },
  "results": <the actual data returned from MongoDB>,
  "result_type": "table | metric | update_confirmation",
  "columns": ["col1", "col2"],
  "mongodb_advantage": "Why MongoDB handles this natively and elegantly",
  "oracle_apex_equivalent": "Exactly what Oracle APEX + Oracle DB would require to do the same thing — be specific about PL/SQL, DDL, licenses, and steps needed"
}

Be specific and honest. Show real MongoDB pipelines. Make the Oracle comparison factual and concrete.
Do not invent data — only return what the MongoDB tools actually return."""


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
        "prompt": "Add an EV charging capability field to petrol & diesel dealers. Set ev_charging_available to true for 40% of them randomly, and false for the rest. Then show me a summary of how many dealers have EV charging by state.",
    },
    {
        "id": "territory_performance",
        "label": "Territory Performance",
        "icon": "bi-bar-chart-fill text-primary",
        "prompt": "Show territory performance scorecard — for each state, calculate the average compliance score, average customer rating, total number of dealers, and total outstanding balance. Rank by compliance score worst first so we know where to focus.",
    },
]


def run_vibe_agent(prompt: str) -> dict:
    """
    Run the Claude agent with MongoDB MCP tools against the given prompt.
    Returns a structured dict with results, query, and comparison.
    """
    client = _get_client()
    messages = [{"role": "user", "content": prompt}]
    tool_calls_log = []
    max_iterations = 8

    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        # Append assistant response to message history
        messages.append({"role": "assistant", "content": response.content})

        # If no tool use — agent is done, extract final text
        if response.stop_reason == "end_turn":
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text = block.text
                    break
            # Parse JSON from final response
            try:
                start = final_text.find("{")
                end   = final_text.rfind("}") + 1
                result = json.loads(final_text[start:end])
                result["tool_calls_log"] = tool_calls_log
                return result
            except Exception:
                return {
                    "title": "Response",
                    "summary": final_text,
                    "mongodb_query": {},
                    "results": [],
                    "result_type": "table",
                    "columns": [],
                    "mongodb_advantage": "",
                    "oracle_apex_equivalent": "",
                    "tool_calls_log": tool_calls_log,
                }

        # Process tool_use blocks
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_name  = block.name
                tool_input = block.input
                tool_calls_log.append({"tool": tool_name, "input": tool_input})

                if tool_name in TOOL_REGISTRY:
                    try:
                        result = TOOL_REGISTRY[tool_name](**tool_input)
                    except Exception as e:
                        result = {"error": str(e)}
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            messages.append({"role": "user", "content": tool_results})

    return {
        "title": "Timeout",
        "summary": "Agent reached maximum iterations.",
        "results": [],
        "result_type": "table",
        "columns": [],
        "tool_calls_log": tool_calls_log,
    }
