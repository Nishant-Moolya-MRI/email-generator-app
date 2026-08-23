from agent_server.agent.main import run_graph
from agent_server.server.main import run_server
import asyncio

def main() -> None:
    print("Hello from agent-server!")
    # asyncio.run(run_graph())
    run_server()
