from langchain_experimental.llms.ollama_functions import OllamaFunctions
from Function import BaseFunction, functions_to_json
import os
import json

class ChatOllamaFunctions:
    model: OllamaFunctions
    functions: list[BaseFunction]
    
    def __init__(self, functions: list[BaseFunction], model: str, prompt_template: str = None):
        self.model = OllamaFunctions(model=model, tool_system_prompt_template=prompt_template)
        self.functions = []
        self.__load_functions(_functions=functions)
        
    def __load_functions(self, _functions: list[BaseFunction]):
        self.functions = _functions
        self.model = self.model.bind(functions=functions_to_json(funcs=self.functions))
    
    def __get_vector_memory(self, model:str, redis_url: str = os.getenv("REDIS_URL"), 
                            index_name: str = os.getenv("INDEX_NAME")):
        # Define the vector store memory.
        from langchain_community.embeddings import OllamaEmbeddings 
        embeddings = OllamaEmbeddings(model=model)
        from langchain_community.vectorstores.redis import Redis  
        redis_vectorstore = Redis(redis_url=redis_url, embedding=embeddings, index_name=index_name)
        retriever = redis_vectorstore.as_retriever(search_type="mmr", 
                                                search_kwargs={'k': 3, 'fetch_k': 50}) # Define the retriever for the vector store.
        from langchain.memory import VectorStoreRetrieverMemory  
        vector_memory = VectorStoreRetrieverMemory(retriever=retriever, 
                                                memory_key="history", 
                                                input_key="input") # Define the memory for the vector store.
        return vector_memory
    
    def invoke(self, input: str):
        return self.model.invoke(input)
    
    def run(self, input: str) -> str:
        resp = self.invoke(input)
        resp_function_call = resp.additional_kwargs["function_call"]
        function_name: str = resp_function_call["name"]
        function_arguments: dict = json.loads(resp_function_call["arguments"])
        for function in self.functions:
            if function.name == function_name:
                return function(function_arguments)