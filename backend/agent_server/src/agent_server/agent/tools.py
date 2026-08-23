from agent_server.logger import logger
from langchain_core.tools import BaseTool
from typing import List
from agent_server.agent.mcp_client import mcp_clients
import asyncio

async def get_tools() -> List[BaseTool]:
    try:
        if not mcp_clients:
            raise Exception("MCP client not initialized")
        mcp_tools = await mcp_clients.get_tools()
        final_tools = [] + mcp_tools
        logger.info(f"{len(final_tools)} tools retrieved")
        return final_tools
    except Exception as e:
        logger.error(f"Error in getting tools: {e}")
        return []

toolset = asyncio.run(get_tools())