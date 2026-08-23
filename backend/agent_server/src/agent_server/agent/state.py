from langgraph.graph import MessagesState
from typing import Dict

class GraphState(MessagesState):
    receiver_mail: str
    sender_mail: str
    email_tone: str
    data_points: str
    drafted_mail: Dict
    is_input_valid: bool = False
