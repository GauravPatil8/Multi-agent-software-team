from src.llm import llm
from src.graph.state import ProjectState
from src.schemas.qa_schema import QASchema


structured_llm = llm.with_structured_output(QASchema)


async def qa_node(state:ProjectState):
    prompt=f"""
    You are the QA Engineer of an AI software development team.
    
    Your responsibility is to evaluate the implementation.
    
    Requirement:
    {state["requirement"]}

    Persistent project memory:
    {state["project_memory"]}
    
    Architecture:
    {state["architecture"]}
    
    Research:
    {state["research"]}
    
    Implementation:
    {state["implementation"]}
    
    Tech Lead Review:
    {state["review"]}
    
    Evaluate:
    
    - Requirement coverage
    - Logical correctness
    - Missing functionality
    - API problems
    - Architecture violations
    - Obvious edge cases
    - Obvious security concerns
    
    Do not modify the code.
    
    Decide whether the implementation passes QA.
    
    """
    
    result = await structured_llm.ainvoke(prompt)
    
    return {
        **state,
        "qa":result.model_dump()
    }
    