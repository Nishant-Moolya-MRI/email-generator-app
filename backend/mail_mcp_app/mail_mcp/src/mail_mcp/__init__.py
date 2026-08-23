from mail_mcp.main import run_mcp_server
from mail_mcp.utils.logger import logger

def main() -> None:
    try:
        logger.info("Starting mail-mcp!")
        run_mcp_server()
    except Exception as e:
        logger.error(f"Could not start the mcp server: {e}")
