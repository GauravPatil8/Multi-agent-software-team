from fastapi import FastAPI
from src.graph.workflow import graph
from pydantic import BaseModel

class ProjectRequest(BaseModel):
    requirement: str

app = FastAPI(
    title="Multi Agent AI software development team"
)

@app.get("/")
def root():
    return {
        "message": "server started"
    }

@app.post("/projects")
async def create_project(request:ProjectRequest):
    initial_state={
        "requirement":request.requirement,
        "next_agent":"",
        "architecture":None,
        "research":None,
        "implementation":None,
        "review":None,
        "qa":None,
        "iteration":0,
        "supervisor_reason":""
    }
    
    result = await graph.ainvoke(initial_state)
    
    return {
        "requirement":result["requirement"],
        "architecture":result["architecture"],
        "research":result["research"],
        "implementation":result["implementation"],
        "qa":result["qa"],
        "iteration":result["iteration"],
        "review":result["review"]
    }