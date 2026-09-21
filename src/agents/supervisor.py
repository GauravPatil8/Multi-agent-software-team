from src.llm import llm
from src.schemas.supervisor_schema import SupervisorDecision
from src.graph.state import ProjectState


decision_llm = llm.with_structured_output(SupervisorDecision)

async def supervisor_node(state: ProjectState):
    prompt = f"""
    You are the Tech Lead of an AI software development team.
    
    Your responsibilty is to decide what should happen next.
    
    Project requirement:
    {state["requirement"]}
    
    Architecture:
    {state["architecture"]}
    
    Research:
    {state["research"]}
    
    Available agents:
    
    architect:
    Designs the technical architecture.
    
    researcher:
    Researches technologies , libraries , best practices and technical risks.
    
    developer:
    Implements the software
    
    qa:
    Tests and evaluates the implementation.
    
    end:
    Ends the workflow.
    
    
    Rules:
    - If architecture is missiing , choose architect.
    - If architecture exists but research is missing , choose researcher.
    - If research exists but implementation is missing , choose developer.
    - If implementation exists but has not been reviewed, choose developer or qa according to the  Tech Lead Review
    - If QA has passed , choose end.
    
    Return a structured decision.
    
    """

    decision = decision_llm.ainvoke(prompt)

    return {
        **state,
        "next_agent": decision.next_agent,
        "supervisior_reason": decision.reason
    }