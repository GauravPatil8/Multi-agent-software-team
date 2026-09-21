from typing import TypedDict

class ProjectState(TypedDict):
    requirement: str
    next_agent: str
    supervisor_reason:str
    