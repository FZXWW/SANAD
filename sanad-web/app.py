from __future__ import annotations

import math
import threading
from typing import Any

import pandas as pd
from flask import Flask, jsonify, render_template, request

from SANAD_AI_FULL_SYSTEM import SanadAIFullSystem


app = Flask(__name__)

system = SanadAIFullSystem()
training_state: dict[str, Any] = {
    "ready": False,
    "training": False,
    "error": None,
}
_training_lock = threading.Lock()


CATEGORY_LABELS = {
    "Deposits": "الودائع والمنتجات الادخارية",
    "Saudi_Funds": "الصناديق الاستثمارية السعودية",
    "Saudi_Stocks": "سوق الأسهم السعودي",
    "US_Stocks": "سوق الأسهم الأمريكي",
    "Mixed": "محفظة مختلطة",
}


def clean_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def frame_to_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    if frame is None or frame.empty:
        return []
    records = frame.to_dict(orient="records")
    return [
        {key: clean_value(value) for key, value in record.items()}
        for record in records
    ]


def start_training() -> None:
    with _training_lock:
        if training_state["ready"] or training_state["training"]:
            return
        training_state.update({"training": True, "error": None})
        try:
            system.train_all()
            training_state.update({"ready": True, "training": False, "error": None})
        except Exception as exc:  # pragma: no cover - exposed to UI for local debugging
            training_state.update({"ready": False, "training": False, "error": str(exc)})


def ensure_training_started() -> None:
    if training_state["ready"] or training_state["training"]:
        return
    thread = threading.Thread(target=start_training, daemon=True)
    thread.start()


def parse_user_profile(payload: dict[str, Any]) -> dict[str, Any]:
    required = [
        "age",
        "monthly_income",
        "investment_capital",
        "investment_horizon",
        "risk_tolerance",
        "investment_goal",
        "experience_level",
        "liquidity_need",
    ]
    missing = [field for field in required if payload.get(field) in (None, "")]
    if missing:
        raise ValueError("الرجاء تعبئة جميع الحقول المطلوبة.")

    return {
        "age": int(payload["age"]),
        "monthly_income": float(payload["monthly_income"]),
        "investment_capital": float(payload["investment_capital"]),
        "investment_horizon": payload["investment_horizon"],
        "risk_tolerance": payload["risk_tolerance"],
        "investment_goal": payload["investment_goal"],
        "preferred_market": payload.get("preferred_market") or "Both",
        "experience_level": payload["experience_level"],
        "liquidity_need": payload["liquidity_need"],
    }


@app.get("/")
def index():
    ensure_training_started()
    return render_template("index.html")


@app.get("/api/status")
def status():
    ensure_training_started()
    return jsonify(training_state)


@app.get("/api/models")
def models():
    if not training_state["ready"]:
        return jsonify({"ready": False, "models": []})

    model_rows = []
    for name, results in system.model_results().items():
        best = results.iloc[0].to_dict()
        model_rows.append(
            {
                "scope": name,
                "best_model": best.get("Model"),
                "accuracy": clean_value(best.get("Accuracy")),
                "f1_score": clean_value(best.get("F1 Score")),
            }
        )
    return jsonify({"ready": True, "models": model_rows})


@app.post("/api/recommend")
def recommend():
    if not training_state["ready"]:
        return jsonify({"message": "النظام لا يزال يدرّب النماذج. انتظر قليلا ثم أعد المحاولة."}), 503

    try:
        user_profile = parse_user_profile(request.get_json(force=True))
        result = system.recommend(user_profile, top_n=5)
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400
    except Exception as exc:  # pragma: no cover - local project surface
        return jsonify({"message": f"تعذر توليد التوصية: {exc}"}), 500

    category = result["recommended_category"]
    confidence = clean_value(result["category_confidence"])
    return jsonify(
        {
            "recommended_category": category,
            "recommended_category_ar": CATEGORY_LABELS.get(category, category),
            "category_confidence": confidence,
            "final_recommendations": frame_to_records(result["final_recommendations"]),
        }
    )


if __name__ == "__main__":
    ensure_training_started()
    app.run(host="127.0.0.1", port=5000, debug=True)
