from langchain_openai.chat_models import ChatOpenAI
from mail_mcp.config import settings
from mail_mcp.utils.logger import logger

LLM_MODEL_NAME = "gpt-5.4-mini"

async def create_llm() -> ChatOpenAI:
    try:
        llm = ChatOpenAI(
            model=LLM_MODEL_NAME,
            base_url=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
        )
        logger.info("LLM initialized")
        return llm
    except Exception as e:
        logger.error(f"LLM couldn't be initialized: {e}")
        return None