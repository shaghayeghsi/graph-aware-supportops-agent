from app.agents.nodes import classify_node
def test_order_intent_and_id():
    result = classify_node({"message": "My order ORD-5001 is late", "trace": []})
    assert result["intent"] == "order_status"
    assert result["order_id"] == "ORD-5001"
def test_return_intent():
    assert classify_node({"message": "I want a refund", "trace": []})["intent"] == "return_request"
