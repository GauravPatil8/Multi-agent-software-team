from src.llm import llm
from src.graph.state import ProjectState
from src.schemas.research_schema import ResearchSchema

structured_llm = llm.with_structured_output(ResearchSchema)

async def researcher_node(state:ProjectState):
    prompt=f"""
    You are the Researcher of an AI software development team.
    
    Your responsibility is to research technical choices relevant to the project.
    
    Project requirement:
    {state["requirement"]}
    
    Current architecture:
    {state["architecture"]}
    
    Research:
    
    - Appropriate technologies
    - Useful libraries
    - Best Practices
    - Potential technical risks.
    
    Do not write implementation code.
    
    Provide useful findings and recommendations for the developer.
    """
    
    result = await structured_llm.ainvoke(prompt)
    
    return {
        **state,
        "research":result.model_dump()
    }