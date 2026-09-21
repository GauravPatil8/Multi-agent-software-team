from pydantic import BaseModel,Field

class ResearchSchema(BaseModel):
    findings:list[str]=Field(description="Important technical findings.")
    recommendations:list[str]=Field(description="Recommended technologies , libraries and approaches")
    considerations:list[str]=Field(description="Important risks or considerations.")