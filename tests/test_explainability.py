from app.explainability.shapley_explainer import explain_escalation, shapley_values
def test_attributions_sum_to_score():
    x = {"repeat_contact": 1, "delivery_delay": 1, "negative_sentiment": 0}
    result = explain_escalation(x)
    assert abs(sum(shapley_values(x).values()) - result["score"]) < 1e-9
def test_all_signals_trigger_escalation():
    assert explain_escalation({"repeat_contact": 1, "delivery_delay": 1,
                               "negative_sentiment": 1})["escalate"]
