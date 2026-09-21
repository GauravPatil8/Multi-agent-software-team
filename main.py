from fastapi import FastAPI, HTTPException
from src.graph.workflow import graph
from src.memory.project_memory import load_project_memory, save_project_memory
from pydantic import BaseModel
from pathlib import Path

class ProjectRequest(BaseModel):
    requirement: str
    project_directory: str

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
    project_directory = Path(request.project_directory).expanduser().resolve()
    if not project_directory.is_dir():
        raise HTTPException(
            status_code=400,
            detail="project_directory must be an existing directory",
        )

    initial_state={
        "requirement":request.requirement,
        "project_directory":str(project_directory),
        "project_memory":load_project_memory(str(project_directory)),
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
    save_project_memory(str(project_directory), result)
    
    return {
        "requirement":result["requirement"],
        "architecture":result["architecture"],
        "research":result["research"],
        "implementation":result["implementation"],
        "qa":result["qa"],
        "iteration":result["iteration"],
        "review":result["review"]
    }