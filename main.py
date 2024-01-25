from dotenv import load_dotenv
import os

load_dotenv(override=True)
        
from ChatOllamaFunctions import ChatOllamaFunctions
from functions import weather, chat, search
    
def load_personality() -> str:
    personality: str = ""
    with open(os.getenv("PERSONALITY_FILE")) as f:
        personality = f.read()
    return personality

def load_system_prompt_template() -> str:
    template: str = ""
    with open(os.getenv("SYS_PROMPT_FILE")) as f:
        template = f.read()
    return template

MODEL = os.getenv("MODEL")
chat_llm: ChatOllamaFunctions = ChatOllamaFunctions(
    functions=[
        weather.WeatherFunction(), 
        chat.ChatFunction(personality=load_personality()),
        search.SearchFunction(model=MODEL, personality=load_personality())
        ], 
    model=MODEL,
    prompt_template=load_system_prompt_template())

