from dotenv import load_dotenv
import os

load_dotenv(override=True)
        
from ChatOllamaFunctions import ChatOllamaFunctions
from Function import json_to_functions
from functions import weather, chat, search
import json

func_json = None
with open(os.getenv("FUNC_FILE")) as f:
    func_json = json.load(f)
    
def load_personality() -> str:
    personality: str = ""
    with open(os.getenv("PERSONALITY_FILE")) as f:
        personality = f.read()
    return personality

MODEL = os.getenv("MODEL")
funcs = json_to_functions(func_json=func_json)
chat_llm: ChatOllamaFunctions = ChatOllamaFunctions(
    functions=[
        weather.WeatherFunction(), 
        chat.ChatFunction(personality=load_personality()),
        search.SearchFunction(model=MODEL)
        ], 
    model=MODEL)

print(f'{chat_llm.run("How are you today?")}')

