from langchain_mcp_adapters.client import MultiServerMCPClient
from agent_server.logger import logger
from agent_server.config import settings

def get_mcp_clients() -> MultiServerMCPClient | None:
    try:
        client = MultiServerMCPClient(
            {
                "mail_server": {
                    "transport": "streamable_http",
                    "url": settings.MAIL_MCP_SERVER_URL,
                },
            }
        )
        return client
    except Exception as e:
        logger.error(f"Failed to connect to mcp servers: {e}")
        return None

mcp_clients = get_mcp_clients()
