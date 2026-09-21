from src.graph.state import ProjectState
from langgraph.graph import StateGraph, START, END
from src.agents.supervisor import supervisor_node


builder = StateGraph(ProjectState)

builder.add_node("supervisor", supervisor_node)
builder.add_edge(START, "supervisor")
