from mail_mcp.utils.logger import logger
from mail_mcp.models.mail import SendMailResponse, SendMailRequest, GenerateMailRequest, GenerateMailResponse
from mail_mcp.agents.mail_generator_agent import get_mail_generator_agent
from langchain_core.messages import HumanMessage

DEVELOPMENT_MODE = True

async def generate_mail(params: GenerateMailRequest) -> GenerateMailResponse:
    """
    Tool used to generate email content based on the given parameters
    """
    try:
        email_tone = params.email_tone
        data_points = params.data_points
        additional_description = params.additional_description or ""

        agent = await get_mail_generator_agent()
        if not agent:
            raise Exception("Mail agent not found")

        result = dict()
        if not DEVELOPMENT_MODE:
            result = await agent.ainvoke({
                        "messages": [
                            HumanMessage(content=f"Email tone: {email_tone}\n Data points: {data_points}\n Additional Description: {additional_description}")
                        ]
                    })
        else:
            result["structured_response"] = GenerateMailResponse(subject='Update on Quarterly Sales Performance', body_content='Dear John Lee,\n\nI wanted to provide you with a brief update on our quarterly sales performance. We saw a 10% decrease in sales this quarter, and I wanted to bring this to your attention.\n\nI am reviewing the contributing factors and will work on identifying possible actions to help improve results in the next quarter. Please let me know if you would like to discuss this further.\n\nBest regards,\nNishant')
        
        logger.info("Email generated successfully", result["structured_response"])
        return result["structured_response"]
    except Exception as e:
        logger.error(f"Error generating email: {e}")
        return GenerateMailResponse(subject="", body_content="")


async def send_email(params: SendMailRequest) -> SendMailResponse:
    """
    Tool used to send email based on the given parameters
    """
    try:
        logger.info("Email sent")
        return SendMailResponse(message="Email sent", status="success")
    except Exception as e:
        logger.error(f"Tool Error - while sending email: {e}")
        return SendMailResponse(message="Email_Send_Error", status="error")