from flask import Flask, request, jsonify
from flask_cors import CORS
from mdadss import MDADSS
from domains.ground import GroundScenario
import traceback

app = Flask(__name__)
CORS(app)

system = MDADSS()


@app.route("/")
def home():
    return "MD-ADSS API Running"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)
        scenario_type = data.get("scenario", "defensive")

        # ---- Create Scenario ----
        if scenario_type == "defensive":
            state = GroundScenario.create_defensive_scenario()
        else:
            state = GroundScenario.create_defensive_scenario()

        # ---- Generate Recommendations ----
        raw_recommendations = system.generate_recommendations(state, top_k=3)

        # ---- Normalize Structure (CRITICAL FIX) ----
        recommendations = []

        for i, rec in enumerate(raw_recommendations):

            utility = rec.get("utility") or rec.get("value") or 0
            actions = rec.get("actions", [])
            risk_score = rec.get("risk_score") or rec.get("risk") or 0
            explanation = rec.get("explanation", {})

            normalized = {
                "rank": i + 1,
                "utility": float(utility),
                "actions": actions,
                "risk_score": float(risk_score),
                "explanation": {
                    "expected_gain": explanation.get("expected_gain", 0),
                    "worst_case": explanation.get("worst_case", 0),
                    "fuel_remaining": explanation.get("fuel_remaining", 0),
                    "enemy_health_after": explanation.get("enemy_health_after", 0)
                }
            }

            recommendations.append(normalized)

        # ---- Performance Stats ----
        stats = system.get_performance_stats()

        # Guarantee stat structure
        safe_stats = {
            "bfs": {"nodes_expanded": stats.get("bfs", {}).get("nodes_expanded", 0)},
            "astar": {"nodes_expanded": stats.get("astar", {}).get("nodes_expanded", 0)},
            "minimax": {"nodes_expanded": stats.get("minimax", {}).get("nodes_expanded", 0)},
            "alphabeta": {"nodes_expanded": stats.get("alphabeta", {}).get("nodes_expanded", 0)},
        }

        return jsonify({
            "recommendations": recommendations,
            "stats": safe_stats
        })

    except Exception as e:
        print("ERROR IN /analyze:")
        traceback.print_exc()

        return jsonify({
            "error": "Internal server error",
            "recommendations": [],
            "stats": {
                "bfs": {"nodes_expanded": 0},
                "astar": {"nodes_expanded": 0},
                "minimax": {"nodes_expanded": 0},
                "alphabeta": {"nodes_expanded": 0}
            }
        }), 500


if __name__ == "__main__":
    app.run(port=5000)