from src.llm import llm
from src.schemas.supervisor_schema import SupervisorDecision, CodeReview
from src.graph.state import ProjectState


decision_llm = llm.with_structured_output(SupervisorDecision)
review_llm = llm.with_structured_output(CodeReview)

MAX_ITERATIONS = 5

async def review_code(state:ProjectState):
    prompt=f"""
    You are the Tech Lead reviewing code produced by a Developer.
    
    Requirement:
    {state["requirement"]}
    
    Architecture:
    {state["architecture"]}
    
    Reseach:
    {state["research"]}
    
    Implementation:
    {state["implementation"]}
    
    Review the implementation.
    
    Important rules:

    1. Only evaluate functionality explicitly required by the requirement.
    2. Do NOT require authentication unless the requirement explicitly asks for it.
    3. Do NOT require Redis unless explicitly required.
    4. Do NOT require Docker unless explicitly required.
    5. Do NOT require CI/CD unless explicitly required.
    6. Do NOT require logging infrastructure unless explicitly required.
    7. Do NOT require monitoring or observability unless explicitly required.
    8. Do NOT require Alembic unless explicitly required.
    9. Do NOT add production features that are outside the requirement.
    10. Do not redesign the architecture.
    11. Focus on whether the implementation actually works.
    
    Do not rewrite the code.
    
    Return ONLY the structured CodeReview object.

    Do not return Markdown.
    Do not return a table.
    Do not return prose outside the structured response.    
    
    """
    
    result = await review_llm.ainvoke(prompt)
    
    return result

async def supervisor_node(state:ProjectState):

    if state["iteration"] >= MAX_ITERATIONS:
        return {
            **state,
            "next_agent":"end",
            "supervisor_reason":(
                "Maximum iteration limit reached."
            )
        }
    
    if state["implementation"] and state["review"] is None:
        review = await review_code(state)
        
        if review.approved:
            next_agent = "qa"
        else:
            next_agent = "developer"
        
        return {
            **state,
            "review":review.model_dump(),
            "next_agent":next_agent,
            "supervisor_reason":"Tech Lead completed the code review."
        }
        
    if state["qa"] is not None:
        if not state["qa"]["passed"]:
            return {
                **state,
                "next_agent":"developer",
                "supervisor_reason":"QA found problems that require fixes.",
                "review":None,
                "qa":None
            }
        
        return {
            **state,
            "next_agent":"end",
            "supervisor_reason":"QA passed . The implementation is completed."
        }
    
    prompt=f"""
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
    
    decision = await decision_llm.ainvoke(prompt)
    
    return {
        **state,
        "next_agent":decision.next_agent,
        "supervisor_reason":decision.reason
    }