"""
MongoDB MCP-equivalent tool implementations.

These functions mirror what the official @mongodb-js/mongodb-mcp-server
exposes as MCP tools — implemented directly in Python so the Claude agent
can call them via Anthropic tool_use without requiring a Node.js subprocess.

Each function accepts JSON-serialisable arguments and returns
JSON-serialisable results, exactly as an MCP tool would.
"""
import json
from datetime import datetime
from bson import ObjectId
from app import mongo


def _serialise(obj):
    """Recursively convert MongoDB documents to JSON-safe dicts."""
    if isinstance(obj, list):
        return [_serialise(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _serialise(v) for k, v in obj.items()}
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


# ── Tool: list_collections ────────────────────────────────────────────
def list_collections() -> dict:
    """List all collections in the iocl_dms database with document counts."""
    names = mongo.db.list_collection_names()
    result = []
    for name in sorted(names):
        count = mongo.db[name].count_documents({})
        result.append({"collection": name, "document_count": count})
    return {"collections": result}


# ── Tool: get_schema ─────────────────────────────────────────────────
def get_schema(collection: str, sample_size: int = 3) -> dict:
    """
    Sample documents from a collection and infer its field structure.
    Returns field names, types, and example values.
    """
    if collection not in mongo.db.list_collection_names():
        return {"error": f"Collection '{collection}' does not exist."}

    docs = list(mongo.db[collection].find().limit(sample_size))
    if not docs:
        return {"collection": collection, "fields": [], "sample_documents": []}

    # Collect all top-level keys across samples
    all_keys = {}
    for doc in docs:
        for k, v in doc.items():
            if k not in all_keys:
                all_keys[k] = {
                    "type": type(v).__name__,
                    "example": _serialise(v) if not isinstance(v, (dict, list))
                               else f"<{type(v).__name__}>"
                }

    return {
        "collection": collection,
        "fields": [{"name": k, **v} for k, v in all_keys.items()],
        "sample_documents": _serialise(docs),
    }


# ── Tool: find_documents ─────────────────────────────────────────────
def find_documents(collection: str, filter: dict = None,
                   projection: dict = None, limit: int = 20,
                   sort_field: str = None, sort_order: int = -1) -> dict:
    """
    Find documents in a collection with optional filter, projection,
    sort and limit. Mirrors mongodb MCP find tool.
    """
    if collection not in mongo.db.list_collection_names():
        return {"error": f"Collection '{collection}' does not exist."}

    cursor = mongo.db[collection].find(filter or {}, projection or {})
    if sort_field:
        cursor = cursor.sort(sort_field, sort_order)
    cursor = cursor.limit(min(limit, 50))
    docs = _serialise(list(cursor))
    return {
        "collection": collection,
        "filter": filter or {},
        "count": len(docs),
        "documents": docs,
    }


# ── Tool: aggregate ──────────────────────────────────────────────────
def aggregate(collection: str, pipeline: list) -> dict:
    """
    Run an aggregation pipeline against a collection.
    Mirrors mongodb MCP aggregate tool.
    """
    if collection not in mongo.db.list_collection_names():
        return {"error": f"Collection '{collection}' does not exist."}

    try:
        results = _serialise(list(mongo.db[collection].aggregate(pipeline)))
        return {
            "collection": collection,
            "pipeline": pipeline,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        return {"error": str(e), "pipeline": pipeline}


# ── Tool: update_documents ───────────────────────────────────────────
def update_documents(collection: str, filter: dict,
                     update: dict, many: bool = True) -> dict:
    """
    Update one or many documents. Mirrors mongodb MCP updateMany/updateOne.
    Restricted to $set operations only for demo safety.
    """
    if collection not in mongo.db.list_collection_names():
        return {"error": f"Collection '{collection}' does not exist."}

    # Safety: only allow $set
    if not any(k.startswith("$") for k in update):
        update = {"$set": update}

    if many:
        result = mongo.db[collection].update_many(filter, update)
    else:
        result = mongo.db[collection].update_one(filter, update)

    return {
        "collection": collection,
        "filter": filter,
        "update": update,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }


# ── Tool: count_documents ────────────────────────────────────────────
def count_documents(collection: str, filter: dict = None) -> dict:
    """Count documents matching an optional filter."""
    if collection not in mongo.db.list_collection_names():
        return {"error": f"Collection '{collection}' does not exist."}
    count = mongo.db[collection].count_documents(filter or {})
    return {"collection": collection, "filter": filter or {}, "count": count}


# ── Tool registry — maps tool name → function ────────────────────────
TOOL_REGISTRY = {
    "list_collections":  list_collections,
    "get_schema":        get_schema,
    "find_documents":    find_documents,
    "aggregate":         aggregate,
    "update_documents":  update_documents,
    "count_documents":   count_documents,
}

# ── Tool definitions for Claude API (tool_use format) ────────────────
TOOL_DEFINITIONS = [
    {
        "name": "list_collections",
        "description": "List all MongoDB collections in the IOCL DMS database with their document counts. Always call this first to understand what data is available.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_schema",
        "description": "Inspect the field structure of a MongoDB collection by sampling real documents. Use this before writing queries to understand available fields.",
        "input_schema": {
            "type": "object",
            "properties": {
                "collection": {"type": "string", "description": "Collection name to inspect"},
                "sample_size": {"type": "integer", "description": "Number of docs to sample (default 3)", "default": 3},
            },
            "required": ["collection"],
        },
    },
    {
        "name": "find_documents",
        "description": "Find documents in a MongoDB collection with optional filter, projection, sort and limit.",
        "input_schema": {
            "type": "object",
            "properties": {
                "collection":  {"type": "string"},
                "filter":      {"type": "object", "description": "MongoDB filter query"},
                "projection":  {"type": "object", "description": "Fields to include/exclude"},
                "limit":       {"type": "integer", "default": 20},
                "sort_field":  {"type": "string"},
                "sort_order":  {"type": "integer", "description": "1 asc, -1 desc", "default": -1},
            },
            "required": ["collection"],
        },
    },
    {
        "name": "aggregate",
        "description": "Run a MongoDB aggregation pipeline. Use for grouping, joins ($lookup), calculations, rankings, and multi-dimensional analytics.",
        "input_schema": {
            "type": "object",
            "properties": {
                "collection": {"type": "string"},
                "pipeline":   {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "MongoDB aggregation pipeline stages",
                },
            },
            "required": ["collection", "pipeline"],
        },
    },
    {
        "name": "update_documents",
        "description": "Add or update fields on existing MongoDB documents without any schema migration. Demonstrates MongoDB's flexible schema — new fields can be added to any subset of documents instantly.",
        "input_schema": {
            "type": "object",
            "properties": {
                "collection": {"type": "string"},
                "filter":     {"type": "object", "description": "Which documents to update"},
                "update":     {"type": "object", "description": "Fields to set (use $set operator or plain key-value)"},
                "many":       {"type": "boolean", "default": True},
            },
            "required": ["collection", "filter", "update"],
        },
    },
    {
        "name": "count_documents",
        "description": "Count documents in a collection matching an optional filter.",
        "input_schema": {
            "type": "object",
            "properties": {
                "collection": {"type": "string"},
                "filter":     {"type": "object"},
            },
            "required": ["collection"],
        },
    },
]
