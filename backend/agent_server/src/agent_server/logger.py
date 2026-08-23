import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler("/tmp/agent_server.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger("agent_server")