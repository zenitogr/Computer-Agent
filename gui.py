from src.inference.gemini import ChatGemini
from src.agent.computer import ComputerAgent
from src.inference.groq import AudioGroq
from src.speech import Speech
from dotenv import load_dotenv
from ui import launch_app
import os

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
groq_api_key=os.getenv('GROQ_API_KEY')

llm=ChatGemini(model='gemini-2.0-flash',api_key=google_api_key,temperature=0)
audio_llm=AudioGroq(model='whisper-large-v3',mode='translations',api_key=groq_api_key,temperature=0)

speech=Speech(llm=audio_llm,verbose=True)
agent=ComputerAgent(llm=llm,use_vision=False,verbose=True)

launch_app(agent=agent,speech=speech)