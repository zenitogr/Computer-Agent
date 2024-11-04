from src.inference.gemini import ChatGemini
from src.inference.mistral import ChatMistral
from src.inference.groq import ChatGroq
from src.agent.computer import ComputerAgent
from src.agent.memory import MemoryAgent
from src.agent.web import WebSearchAgent
from src.agent.terminal import TerminalAgent
from src.agent.system import SystemAgent
# from src.llm_switcher import LLMSwitcher
from dotenv import load_dotenv
import os

load_dotenv()

# llms=[
#     ChatGemini(model='gemini-1.5-flash',api_key=os.getenv('GOOGLE_API_KEY')),
#     ChatGroq(model='llama-3.1-70b-versatile',api_key=os.getenv('GROQ_API_KEY')),
#     ChatMistral(model='open-codestral-mamba',api_key=os.getenv('MISTRAL_API_KEY'))
# ]

# llm_switcher=LLMSwitcher(llms=llms,max_retries=2)
llm=ChatGemini(model='gemini-1.5-flash',api_key=os.getenv('GOOGLE_API_KEY'))
agent=ComputerAgent(llm=llm,verbose=True)
user_query=input('Enter your query: ')
agent_response=agent.invoke(user_query)
print(agent_response)
