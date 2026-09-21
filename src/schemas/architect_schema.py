from pydantic import BaseModel,Field

class ArchitectSchema(BaseModel):
    summary:str=Field(description="A short summary of the proposed architecture.")
    components:list[str]=Field(description="Major components of the system")
    technologies:list[str]=Field(description="Technologies and framework to use.")
    api_design:list[str]=Field(description="Imporatant API endpoints and their purpose")
    database_design:list[str]=Field(description="Important database tables or models")