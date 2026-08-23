from langchain_azure_ai.agents.hosting import InvocationAgentServerHost
from agent_server.agent.graph import build_graph
import asyncio
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from langchain_core.messages import HumanMessage
from agent_server.agent.state import GraphState

app = InvocationAgentServerHost()

workflow = None

@app.invoke_handler
async def handle_invoke(request: Request) -> Response:
    data = await request.json()

    init_state: GraphState = {
        "sender_mail": data.get("sender_mail", ""),
        "receiver_mail": data.get("receiver_mail", ""),
        "data_points": data.get("data_points", ""),
        "email_tone": data.get("email_tone", "professional"),
        "messages": HumanMessage(content=data.get("message", ""))
    }

    result = await workflow.ainvoke(init_state)

    messages = result.get("messages", [])
    if not result.get("is_input_valid"):
        return JSONResponse({
                "message": messages[-1].content,
                "messages": [m.model_dump() for m in messages]
            })

    return JSONResponse({
        "drafted_mail": result.get("drafted_mail", {}),
        "messages": [m.model_dump() for m in messages]
        })

def run_server():
    global workflow
    workflow = asyncio.run(build_graph())
    app.run(port=8088)