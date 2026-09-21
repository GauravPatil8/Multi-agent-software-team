from langchain_core.messages import HumanMessage, ToolMessage
from src.schemas.developer_schema import DeveloperSchema
from src.graph.state import ProjectState
from src.llm import llm

structured_llm = llm.with_structured_output(DeveloperSchema)


async def _run_file_tools(prompt: str, project_directory: str) -> list[str]:
    from src.tools.file_tools import get_file_tools

    file_tools = get_file_tools(project_directory)
    tool_llm = llm.bind_tools(file_tools)
    messages = [HumanMessage(content=prompt)]
    tool_map = {tool.name: tool for tool in file_tools}
    results = []

    for _ in range(8):
        response = await tool_llm.ainvoke(messages)
        messages.append(response)
        if not response.tool_calls:
            break

        for tool_call in response.tool_calls:
            tool = tool_map.get(tool_call["name"])
            if tool is None:
                result = f"Unknown tool: {tool_call['name']}"
            else:
                try:
                    result = tool.invoke(tool_call["args"])
                except (OSError, ValueError) as error:
                    result = f"Tool error: {error}"
            results.append(str(result))
            messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )

    return results

async def developer_node(state:ProjectState):
    prompt=f"""
    You are the Developer of an AI software development team .
    
    Your responsibility is to implement the software requirement using the architecture and research provided by the team.
    
    Project requirement:
    {state["requirement"]}

    Persistent project memory:
    {state["project_memory"]}
    
    Architecture:
    {state["architecture"]}
    
    Research:
    {state["research"]}
    
    Previous implementation:
    {state["implementation"]}
    
    Previous QA result:
    {state["qa"]}
    
    Previous Tech Lead review:
    {state["review"]}

    Project directory:
    {state["project_directory"]}
    
    Instructions:
    
    - Implement the requirement.
    - Follow the architecture.
    - Use the research recommendations when appropriate.
    - If previous review or QA found problems , fix them .
    - Write practical implementation code.
    - Do not redesign the entire system unnecessarily.
    - Do not write tests yet.
    - Do not add authentication unless explicitly required.
    - Do not add Redis unless explicitly required.
    - Do not add Docker unless explicitly required.
    - Do not add CI/CD unless explicitly required.
    - Do not add unrelated production features
    - First inspect the destination folder with analyze_folder.
    - Use create_file for new files.
    - Use edit_file_lines for targeted edits to existing files; line numbers are 1-based.
    - Use delete_file_lines to remove targeted lines from existing files; line numbers are 1-based and inclusive.
    - Use tools to make the implementation changes, then report every changed file.
    
    IMPORTANT: 
    
    Return ONLY data that matches DeveloperSchema: 
    
    files: 
        path 
        code 
    explanation: 
        short implementation explanation
    """
    
    tool_results = await _run_file_tools(prompt, state["project_directory"])
    result = await structured_llm.ainvoke(
        prompt
        + "\n\nTool execution results:\n"
        + "\n".join(tool_results)
        + "\nReturn the final file contents and explanation after the tool calls."
    )
    
    return {
        **state,
        "implementation":result.model_dump(),
        "iteration":state["iteration"] + 1
    }
    
