from dotenv import load_dotenv
import os

# load environmental variables
load_dotenv(override=True)
        
from ChatOllamaFunctions import ChatOllamaFunctions
from functions import weather, chat, search

def load_from_template(path: str) -> str:
    """
    Load a template from a file and return it as a string.
    Args:
        path (str): The path to the template file.

    Returns:
        str: The template as a string.
    """
    template: str = ""
    with open(path) as f:
        template = f.read()
    return template

MODEL = os.getenv("MODEL")

# Load the templates from the files.
personality_template: str = load_from_template(os.getenv("PERSONALITY_FILE"))
sys_prompt_template: str = load_from_template(os.getenv("SYS_PROMPT_FILE"))

# Create an instance on the ChatOllamaFunctions class.
chat_llm: ChatOllamaFunctions = ChatOllamaFunctions(
    functions=[
        weather.WeatherFunction(), 
        chat.ChatFunction(personality=personality_template),
        search.SearchFunction(model=MODEL, personality=personality_template)
        ], 
    model=MODEL,
    prompt_template=sys_prompt_template)

