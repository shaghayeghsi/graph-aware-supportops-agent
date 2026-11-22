from langgraph.graph import StateGraph, END
from app.agents.state import SupportState
from app.agents import nodes
def build_support_graph(retriever, db):
    graph = StateGraph(SupportState)
    graph.add_node("classify", nodes.classify_node)
    graph.add_node("retrieve", lambda s: nodes.retrieve_node(s, retriever))
    graph.add_node("business", lambda s: nodes.business_node(s, db))
    graph.add_node("decide", lambda s: nodes.decision_node(s, db))
    graph.add_node("respond", nodes.respond_node)
    graph.set_entry_point("classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "business")
    graph.add_edge("business", "decide")
    graph.add_edge("decide", "respond")
    graph.add_edge("respond", END)
    return graph.compile()
