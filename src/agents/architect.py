from src.llm import llm
from src.schemas.architect_schema import ArchitectSchema
from src.graph.state import ProjectState

structured_llm = llm.with_structured_output(ArchitectSchema)

async def architect_node(state:ProjectState):
    prompt=f"""
    You are the Software Architect of an software development team.
    
    Your responsibility is to design the technical architecture.
    
    Project requirement:
    {state["requirement"]}
    
    Create a practical architecture.
    
    Consider.
    - Backend framework
    - Application components
    - APIs
    - Database
    - Technologies
    
    Do not write implemention code.
    
    Focus only on architecture.
    """
    
    result = await structured_llm.ainvoke(prompt)
    
    return {
        **state,
        "architecture":result.model_dump()
    }
