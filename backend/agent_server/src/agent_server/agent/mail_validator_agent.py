from agent_server.agent.llm import create_llm
from agent_server.logger import logger
from langchain.agents import create_agent
from agent_server.agent.output_models import EmailValidationResponse

async def get_validator_agent():
    try:
        llm = await create_llm()
        if not llm:
            raise Exception("No LLM found")
        validation_prompt = """
        You are an input validation agent for an email generation system.

        Your job is to determine whether enough information is available
        to generate the requested email.

        You will receive:
        - sender email
        - receiver email
        - email tone
        - data points
        - user's email description

        Follow these rules:

        1. Sender email is required.
        2. Receiver email is required.
        3. If email tone is missing, use "professional" as the fallback.
        Do not ask the user for a tone.
        4. Determine whether data points are actually necessary based on
        the user's email description.
        5. Do not ask for unnecessary information.
        6. If all necessary information is available, mark the input as VALID.
        7. If required information is missing, mark the input as INVALID and
        clearly ask the user only for the missing information.
        8. Do not generate the email yourself.

        Return the validation result clearly as:

        Status: True

        or:

        Status: False

        If False, clearly explain what information the user needs to provide.
        """
        agent = create_agent(
            model=llm,
            system_prompt=validation_prompt,
            response_format=EmailValidationResponse
        )
        logger.info("Validator agent initialized")
        return agent
    except Exception as e:
        logger.error(f"Validator agent couldn't be initialized: {e}")
        return None