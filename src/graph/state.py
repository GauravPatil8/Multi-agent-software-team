from typing import TypedDict

class ArchitectState(TypedDict):
    summary:str
    components:list[str]
    technologies:list[str]
    api_design:list[str]
    database_design:list[str]

class ResearchState(TypedDict):
    findings:list[str]
    recommendations:list[str]
    considerations:list[str]

class FileChangeState(TypedDict):
    path:str
    code:str
    
class ImplementationState(TypedDict):
    files:list[FileChangeState]
    explanation:str

class QAState(TypedDict):
    passed:bool
    findings:list[str]
    recommendations:list[str]

class ReviewState(TypedDict):
    approved:bool
    issues:list[str]
    recommendations:list[str]

class ProjectState(TypedDict):
    requirement:str
    project_directory:str
    project_memory:dict
    architecture:ArchitectState | None
    research:ResearchState | None
    implementation:ImplementationState | None
    qa:QAState | None
    review:ReviewState | None
    iteration:int
    next_agent:str
    supervisor_reason:str
