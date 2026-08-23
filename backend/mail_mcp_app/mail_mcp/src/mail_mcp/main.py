from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from mail_mcp.tools.mail import send_email, generate_mail
from mail_mcp.utils.logger import logger

mcp = FastMCP(
    name="Mail MCP Server",
    version="v1",
    instructions="""
    An email server that handles sending. It supports SMTP for sending emails. The server is designed to be fast, reliable, and easy to use.
    """
)

mcp.tool()(generate_mail)
# mcp.tool()(send_email)

def run_mcp_server():
    try:
        mcp.run(
            transport="streamable-http",
            middleware=[
                Middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
                    allow_headers=["*"],
                    expose_headers=["Mcp-Session-Id"]
                    )
            ]
        )
    except Exception as e:
        logger.error(f"An error occurred while running mcp server: {e}")
        