from pydantic import BaseModel, Field
from typing import Literal

class SupervisorDecision(BaseModel):
    next_agent: Literal["architect", "researcher", "developer", "qa", "end"]=Field(description="The next agent that should work")
    reason: str = Field(description="Why this particular agent should work next")

class CodeReview(BaseModel):
    approved:bool=Field(description="Whether the implementation is acceptable.")
    issues:list[str]=Field(description="Problems found in the implementation.")
    recommendations:list[str]=Field(description="Recommended improvements or fixes.")