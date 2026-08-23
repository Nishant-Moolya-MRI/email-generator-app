from agent_server.agent.llm import create_llm
from agent_server.logger import logger
from agent_server.agent.tools import toolset

def get_mail_agent_prompt():
    return "You are an email agent. You will be given a receiver's email, sender's email, email tone and data points along with user email description. Your task is to use the necessary tools to complete your task."

async def get_mail_agent():
    try:
        llm = await create_llm()
        if not llm:
            raise Exception("No LLM found")
        agent = llm.bind_tools(toolset)
        logger.info("Email agent initialized")
        return agent
    except Exception as e:
        logger.error(f"Email agent couldn't be initialized: {e}")
        return None