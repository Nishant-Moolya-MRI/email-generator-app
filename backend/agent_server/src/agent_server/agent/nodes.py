from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from agent_server.agent.mail_agent import get_mail_agent, get_mail_agent_prompt
from agent_server.agent.mail_validator_agent import get_validator_agent
from typing import Literal
from langgraph.prebuilt.tool_node import ToolNode
from agent_server.agent.tools import toolset
from agent_server.agent.state import GraphState

async def validator_agent_node(state: GraphState) -> GraphState:
    agent = await get_validator_agent()
    if not agent:
        return {}

    messages = state.get("messages", [])
    user_query = messages[-1].content if messages else ""
    prompt = f"""
    Validate the following email generation request.

    Sender email:
    {state.get("sender_mail", "")}

    Receiver email:
    {state.get("receiver_mail", "")}

    Email tone:
    {state.get("email_tone", "")}

    Data points:
    {state.get("data_points", "")}

    User's email description:
    {user_query}
    """

    result = await agent.ainvoke({
        "messages": [HumanMessage(content=prompt)]
    })

    return {
        "is_input_valid": result["structured_response"].is_valid,
        "messages": [HumanMessage(content=prompt), AIMessage(content=result["structured_response"].message)]
    }

async def mail_agent_node(state: GraphState) -> GraphState:
    agent = await get_mail_agent()
    if not agent:
        return {}
    result = await agent.ainvoke([
                *state.get("messages", []),
                SystemMessage(content=get_mail_agent_prompt()),
                HumanMessage(
                content=f"""Generate the mail based on the following context:
                Sender email: {state.get("sender_mail", "")}
                Receiver email: {state.get("receiver_mail", "")}
                Email tone: {state.get("email_tone", "professional")}
                Data points: {state.get("data_points", "")}
                """
                )
            ])
    return {
        "messages": [result]
    }

tool_node = ToolNode(tools=toolset)

async def route_condition(state: GraphState) -> Literal["__end__", "mail_agent_node"]:
    if state['is_input_valid']:
        return "mail_agent_node"
    return "__end__"

async def save_mail_draft_node(state: GraphState) -> GraphState:
    last_message = state["messages"][-1]
    print(last_message)
    if isinstance(last_message, ToolMessage):
        return {
            "drafted_mail": last_message.artifact.get("structured_content")
        }
    return {}