from langgraph.graph import StateGraph
from orchestration.state import AgentState
from langgraph.constants import END
from agents.architect import architect_agent
from agents.coder import coder_agent
from agents.tester import tester_agent
from agents.reviewer import reviewer_agent
from agents.manager import manager_agent

# build the workflow graph
graph = StateGraph(AgentState)

# add all the agents as nodes
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_node("tester", tester_agent)
graph.add_node("reviewer", reviewer_agent)
graph.add_node("manager", manager_agent)

graph.set_entry_point("architect")

# connect them in sequence
graph.add_edge("architect", "coder")
graph.add_edge("coder", "tester")
graph.add_edge("tester", "reviewer")
graph.add_edge("reviewer", "manager")

def route_decision(state):
    # check what the manager decided
    decision = state.get("decision", "approve")
    # make sure it's a valid decision
    return decision if decision in ["rewrite", "approve"] else "approve"

# conditional edge - loop back to coder if rewrite, otherwise end
graph.add_conditional_edges(
    "manager",
    route_decision,
    {
        "rewrite": "coder",
        "approve": END
    }
)

app = graph.compile()
