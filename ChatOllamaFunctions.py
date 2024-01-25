from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_community.embeddings import OllamaEmbeddings 
from langchain_community.vectorstores.redis import Redis, RedisVectorStoreRetriever
from langchain.memory import VectorStoreRetrieverMemory  
from langchain_core.messages.base import BaseMessage
from Function import BaseFunction, functions_to_json
import os
import json

class ChatOllamaFunctions:
    """
    ChatOllamaFunctions wraps the langchain OllamaFunctions class to 
    allow for easy custom function declaration and invocation.
    """
    model: OllamaFunctions
    functions: list[BaseFunction]
    
    def __init__(self, functions: list[BaseFunction], model: str, prompt_template: str = None):
        """
        Instantiates a new ChatOllamaFunctions object using the given model and prompt.
        Also binds all functions to the llm.
        
        Args:
            functions (list[BaseFunction]): List of functions/ tools the llm can use.
            model (str): The name of the Ollama functional model to use.
            prompt_template (str, optional): Optional prompt the llm can use for picking 
            which function to use. Defaults to None.
        """
        self.model = OllamaFunctions(model=model, tool_system_prompt_template=prompt_template)
        self.functions = []
        self.__load_functions(_functions=functions)
        
    def __load_functions(self, _functions: list[BaseFunction]) -> None:
        """
        __load_functions is a private function that binds all functions to the llm.

        Args:
            _functions (list[BaseFunction]): List of functions/ tools the llm can use.
        """
        self.functions = _functions
        self.model = self.model.bind(functions=functions_to_json(funcs=self.functions))
    
    def __get_vector_memory(self, model:str, redis_url: str = os.getenv("REDIS_URL"), 
                            index_name: str = os.getenv("INDEX_NAME")) -> VectorStoreRetrieverMemory:
        """
        __get_vector_memory is a private function that connects to a redis vector store database 
        and instantiates VectorStoreRetrieverMemory object.

        Args:
            model (str): The name of the OllamaEmbeddings model to use.
            redis_url (str, optional): The redis database connection URL. 
            Defaults to REDIS_URL environmental variable.
            index_name (str, optional): The name of the index to use in the database. 
            Defaults to INDEX_NAME environmental variable.

        Returns:
            VectorStoreRetrieverMemory: The instantiated VectorStoreRetrieverMemory object.
        """
        embeddings: OllamaEmbeddings = OllamaEmbeddings(model=model)
        redis_vectorstore: Redis = Redis(redis_url=redis_url, embedding=embeddings, index_name=index_name)
        # Define the retriever for the vector store.
        retriever: RedisVectorStoreRetriever = redis_vectorstore.as_retriever(search_type="mmr", 
                                                search_kwargs={'k': 3, 'fetch_k': 50})
        # Define the memory for the vector store.
        vector_memory: VectorStoreRetrieverMemory = VectorStoreRetrieverMemory(retriever=retriever, 
                                                memory_key="history", 
                                                input_key="input")
        return vector_memory
    
    def invoke(self, input: str) -> BaseMessage:
        """
        invoke is a function that invokes the llm with the given input. 
        Wraps the OllamaFunctions invoke function.

        Args:
            input (str): The input to invoke the llm with.

        Returns:
            BaseMessage: The response from the llm.
        """
        return self.model.invoke(input)
    
    def run(self, input: str) -> str:
        """
        Wraps the OllamaFunctions invoke function and passes the response to and runs the correct function.  

        Args:
            input (str): The input to invoke the llm with.

        Returns:
            str: The response from the invoked function.
        """
        # invoke the llm with the given input.
        resp: BaseMessage = self.invoke(input)
        resp_function_call: dict = resp.additional_kwargs["function_call"]
        function_name: str = resp_function_call["name"]
        function_arguments: dict = json.loads(resp_function_call["arguments"])
        # call the function with the given name and arguments.
        for function in self.functions:
            if function.name == function_name:
                return function(function_arguments)