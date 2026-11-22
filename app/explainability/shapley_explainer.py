"""Exact Shapley attribution for a small additive escalation score.
This explains this transparent score, not the hidden reasoning of an LLM.
"""
WEIGHTS = {"repeat_contact": 0.40, "delivery_delay": 0.35, "negative_sentiment": 0.25}
def shapley_values(features: dict[str, float]) -> dict[str, float]:
    return {key: weight * float(features.get(key, 0.0)) for key, weight in WEIGHTS.items()}
def explain_escalation(features: dict[str, float]) -> dict:
    attrs = shapley_values(features)
    score = sum(attrs.values())
    return {"score": round(score, 4), "escalate": score >= 0.55,
            "feature_attributions": attrs,
            "note": "Attributions explain the deterministic escalation score, not LLM reasoning."}
