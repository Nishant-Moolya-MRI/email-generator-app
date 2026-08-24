from langgraph.graph import StateGraph, START, END
from agent_server.agent.state import GraphState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.tool_node import tools_condition
from agent_server.agent.nodes import validator_agent_node, mail_agent_node, tool_node, save_mail_draft_node, route_condition

graph = StateGraph(GraphState)

graph.add_node(validator_agent_node)
graph.add_node(mail_agent_node)
graph.add_node("tools", tool_node)
graph.add_node(save_mail_draft_node)

graph.add_edge(START, validator_agent_node.__name__)
graph.add_conditional_edges(validator_agent_node.__name__, route_condition)
graph.add_conditional_edges(mail_agent_node.__name__, tools_condition)
graph.add_edge("tools", save_mail_draft_node.__name__)
graph.add_edge(save_mail_draft_node.__name__, END)

async def build_graph() -> CompiledStateGraph:
    workflow =  graph.compile()
    workflow_img = workflow.get_graph().draw_mermaid_png()
    
    # with open("graph.png", "wb") as f:
    #     f.write(workflow_img)

    return workflow