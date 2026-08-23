from agent_server.agent.graph import build_graph
from agent_server.agent.state import GraphState
from langchain_core.messages import HumanMessage

async def run_graph():
    workflow = await build_graph()
    init_state: GraphState = {
        "sender_mail": "nishant@gmail.com",
        "receiver_mail": "nish@gmail.com",
        "data_points": "sales decreased by 10 percenatge in this quater, manager name is John Lee, sender name is nishant",
        "email_tone": "professional",
        "messages": HumanMessage(content="write a email to my manager")
    }
    result = await workflow.ainvoke(init_state)
    # print("Result State:", result)

    if not result.get("is_input_valid"):
        messages = result.get("messages", [])
        print(f"\nResult: {messages[-1].content if messages else 'Invalid input'}")
        return

    drafted_mail = result.get("drafted_mail")

    if drafted_mail is None:
        print("\nThe agent did not create a mail draft.")
        return

    print(
        f"\nResult:\n"
        f"Subject: {drafted_mail.get("subject", "")}\n\n"
        f"Body: {drafted_mail.get("body_content", "")}"
    )
