from typing import TypedDict,Annotated
from src.message import BaseMessage
from operator import add

class AgentState(TypedDict):
    input:str
    current_agent:str
    messages:Annotated[list[BaseMessage],add]
    agent_data:dict
    agent_response:str
    output:str