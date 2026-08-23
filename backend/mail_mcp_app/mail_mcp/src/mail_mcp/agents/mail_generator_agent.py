from mail_mcp.utils.llm import create_llm
from mail_mcp.models.mail import GenerateMailResponse
from mail_mcp.utils.logger import logger
from langchain.agents import create_agent

async def get_mail_generator_agent():
    try:
        llm = await create_llm()
        if not llm:
            raise Exception("No LLM found")
        agent = create_agent(
            model=llm,
            system_prompt="You are an email generator agent. You will be given the data points, email tone and if needed additional description. Your task is to generate a professional email based on the provided information and the specified email tone. Ensure that the email is clear, concise, and effectively communicates the intended message.",
            response_format=GenerateMailResponse
        )
        logger.info("Email generator agent initialized")
        return agent
    except Exception as e:
        logger.error(f"Email generator agent couldn't be initialized: {e}")
        return None
