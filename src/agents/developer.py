from src.schemas.developer_schema import DeveloperSchema
from src.graph.state import ProjectState
from src.llm import llm

structured_llm = llm.with_structured_output(DeveloperSchema)

async def developer_node(state:ProjectState):
    prompt=f"""
    You are the Developer of an AI software development team .
    
    Your responsibility is to implement the software requirement using the architecture and research provided by the team.
    
    Project requirement:
    {state["requirement"]}
    
    Architecture:
    {state["architecture"]}
    
    Research:
    {state["research"]}
    
    Previous implementation:
    {state["implementation"]}
    
    Previous QA result:
    {state["qa"]}
    
    Previous Tech Lead review:
    {state["review"]}
    
    Instructions:
    
    - Implement the requirement.
    - Follow the architecture.
    - Use the research recommendations when appropriate.
    - If previous review or QA found problems , fix them .
    - Write practical implementation code.
    - Do not redesign the entire system unnecessarily.
    - Do not write tests yet.
    - Do not add authentication unless explicitly required.
    - Do not add Redis unless explicitly required.
    - Do not add Docker unless explicitly required.
    - Do not add CI/CD unless explicitly required.
    - Do not add unrelated production features
    
    IMPORTANT: 
    
    Return ONLY data that matches DeveloperSchema: 
    
    files: 
        path 
        code 
    explanation: 
        short implementation explanation
    """
    
    result = await structured_llm.ainvoke(prompt)
    
    return {
        **state,
        "implementation":result.model_dump(),
        "iteration":state["iteration"] + 1
    }
    
