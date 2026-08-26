from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from mail_mcp.tools.mail import send_email, generate_mail
from mail_mcp.resources.mail import get_generate_mail_ui
from mail_mcp.utils.logger import logger
import os

mcp = FastMCP(
    name="Mail MCP Server",
    version="v1",
    instructions="""
    An email server that handles sending. It supports SMTP for sending emails. The server is designed to be fast, reliable, and easy to use.
    """
)

# resource URIs
resource_uris = {
    "generate_mail_ui" : "ui://draft-mail"
}

# tools
mcp.tool(
    meta={
        "ui": { "resourceUri": resource_uris.get("generate_mail_ui") }
    }
)(generate_mail)
# mcp.tool()(send_email)

# resources
mcp.resource(
    uri=resource_uris.get("generate_mail_ui"),
    description="UI for displaying generated draft mail",
    mime_type="text/html;profile=mcp-app",
)(get_generate_mail_ui)

def run_mcp_server():
    try:
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.getenv("PORT", "8000")),
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
        