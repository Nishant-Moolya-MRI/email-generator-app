import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler("/tmp/mail_mcp.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger("mail_mcp")