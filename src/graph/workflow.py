from src.graph.state import ProjectState
from langgraph.graph import StateGraph, START, END
from src.agents.supervisor import supervisor_node
from src.agents.architect import architect_node
from src.agents.researcher import researcher_node
from src.agents.developer import developer_node
from src.agents.qa import qa_node

def route_from_supervisor(state: ProjectState):
    return state['next_agent']

def route_after_qa(state:ProjectState):
    if state["qa"] and state["qa"]["passed"]:
        return "end"
    return "developer"

builder = StateGraph(ProjectState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("architect", architect_node)
builder.add_node("researcher", researcher_node)
builder.add_node("developer", developer_node)
builder.add_node("qa", qa_node)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", 
                              route_from_supervisor,
                              {
                                  "architect": "architect",
                                  "researcher": "researcher",
                                  "developer": "developer",
                                  "qa": "qa",
                                  "end": END
                              })
builder.add_edge("architect", "supervisor")
builder.add_edge("researcher", "supervisor")
builder.add_edge("developer", "supervisor")

builder.add_conditional_edges("qa",route_after_qa,{"developer":"developer","end":END})


graph = builder.compile()