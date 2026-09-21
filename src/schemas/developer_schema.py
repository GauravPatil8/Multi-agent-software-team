from pydantic import BaseModel, Field

class FileChange(BaseModel):
    path:str=Field(description="Relative path of the file to create or modify.")
    code:str=Field(description="Completed source code for this file.")

class DeveloperSchema(BaseModel):
    files:list[FileChange]=Field(description="Files that should be created or modified.")
    explanation:str=Field(description="Short explanation of the implementation")