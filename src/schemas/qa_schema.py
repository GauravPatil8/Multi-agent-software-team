from pydantic import BaseModel,Field

class QASchema(BaseModel):
    passed:bool=Field(description="whether the implementation passes QA.")
    findings:list[str]=Field(description="Bugs or problems discovered.")
    recommendations:list[str]=Field(description="Changes required if QA fails.")