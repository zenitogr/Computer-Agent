from src.inference.gemini import ChatGemini
from src.agent.computer import ComputerAgent
from dotenv import load_dotenv
import os

load_dotenv()

llm=ChatGemini(model='gemini-1.5-flash',api_key=os.getenv('GOOGLE_API_KEY'))
agent=ComputerAgent(llm=llm,verbose=True)
user_query=input('Enter your query: ')
agent_response=agent.invoke(user_query)
print(agent_response)
