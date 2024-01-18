from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_community.chat_models.ollama import ChatOllama

from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)
REDIS_URL = os.getenv("REDIS_URL")
INDEX_NAME = os.getenv("INDEX_NAME")
MODEL = os.getenv("MODEL")
FUNC_FILE = os.getenv("FUNC_FILE")

class ChatOllamaFunctions:
    model: OllamaFunctions
    
    def __init__(self):
        self.model = OllamaFunctions(model=MODEL)
        self.__load_functions()
        
    def __load_functions(self):
        functions: json = None
        with open(FUNC_FILE) as f:
            functions = json.load(f)
        self.model = self.model.bind(
            functions=functions["functions"]
        )
    
    def __get_vector_memory(self):
        # Define the vector store memory.
        from langchain_community.embeddings import OllamaEmbeddings 
        embeddings = OllamaEmbeddings(model=MODEL)
        from langchain_community.vectorstores.redis import Redis  
        redis_vectorstore = Redis(redis_url=REDIS_URL, embedding=embeddings, index_name=INDEX_NAME)
        retriever = redis_vectorstore.as_retriever(search_type="mmr", 
                                                search_kwargs={'k': 3, 'fetch_k': 50}) # Define the retriever for the vector store.
        from langchain.memory import VectorStoreRetrieverMemory  
        vector_memory = VectorStoreRetrieverMemory(retriever=retriever, 
                                                memory_key="history", 
                                                input_key="input") # Define the memory for the vector store.
        return vector_memory
    
    def invoke(self, input: str):
        return self.model.invoke(input)

print(f'{ChatOllamaFunctions().invoke("Whats the weather in scotland?")}')
