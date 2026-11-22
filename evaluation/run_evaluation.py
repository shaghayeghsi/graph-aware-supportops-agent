from app.agents.nodes import classify_node
CASES = [
    ("Where is my order ORD-5001?", "order_status"),
    ("I want to return this item", "return_request"),
    ("The product arrived broken", "damaged_item"),
    ("What are your opening hours?", "general_question"),
]
def main():
    correct = 0
    for message, expected in CASES:
        actual = classify_node({"message": message, "trace": []})["intent"]
        passed = actual == expected
        correct += int(passed)
        print(f"expected={expected:16s} predicted={actual:16s} pass={passed}")
    print(f"Intent accuracy: {correct}/{len(CASES)} = {correct/len(CASES):.1%}")
if __name__ == "__main__": main()
