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

@app.get("/projects")
async def create_project(request: ProjectRequest):
    initial_state = {
        "requirement": request.requirement,
        "next_agent": "",
        "supervisor_reason": ""
    }

    result = await graph.ainvoke(initial_state)

    return {
        "requirement": result["requirement"]
    }