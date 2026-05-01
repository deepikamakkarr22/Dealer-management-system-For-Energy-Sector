from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.vibe_agent import run_vibe_agent, DEMO_SCENARIOS

vibe_bp = Blueprint("vibe", __name__, url_prefix="/vibe")


@vibe_bp.route("/")
@login_required
def panel():
    return render_template("vibe/panel.html", scenarios=DEMO_SCENARIOS)


@vibe_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    data   = request.get_json(force=True)
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400
    try:
        result = run_vibe_agent(prompt)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
