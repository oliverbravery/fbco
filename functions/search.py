from Function import BaseFunction, Parameter, ParameterType, Property, PropertyType
from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever
from langchain.llms.ollama import Ollama
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate

class SearchFunction(BaseFunction):
    """
    A function derived from the BaseFunction class that allows the llm to search the internet for information.

    Args:
        BaseFunction (_type_): The BaseFunction class to inherit from.
    """
    def __init__(self, model: str, personality: str = ""):
        """
        Instantiates a new SearchFunction object with the given model and personality.

        Example json function call:
        ```json
        {"name": "search", "arguments": {"query": "What is the capital of France?"}}
        ```
        
        Args:
            model (str): The name of the Ollama model to use.
            personality (str, optional): Optional personality the llm can have when responding to the user. Defaults to "".
        """
        self.llm: Ollama = Ollama(model=model)
        self.personaility: str = personality
        super().__init__(name="search", 
                         description="Search the internet for information. Should be used for fact checking and research.", 
                         parameters=[
                             Parameter(type=ParameterType.OBJECT,
                                        properties=[
                                             Property(name="query", 
                                                     type=PropertyType.STRING, 
                                                     attribute={'description': 'The search query or question.'}),
                                        ],
                                        required_parameters=["query"])
                         ])
        
    def __summarise_results(self, query: str, results: list[Document]) -> str:
        """
        __summarise_results is a private function that summarises the results of a search query using StuffDocumentsChain.

        Args:
            query (str): The search query or question.
            results (list[Document]): List of search results to summarise.

        Returns:
            str: The summarised results.
        """
        prompt_template: str = self.personaility+"\nRespond to the users query with a concise summary of the search results: \n users query: "+query+" \nsearch results: {results} \nCONCISE SUMMARY:"
        prompt: PromptTemplate = PromptTemplate.from_template(prompt_template)
        chain: StuffDocumentsChain = StuffDocumentsChain(llm_chain=LLMChain(llm=self.llm, prompt=prompt), document_variable_name="results")
        return chain.run(results)
        
    def __call__(self, arguments: dict) -> str:
        """
        Searches the internet for information using the given query and summarises the results.

        Args:
            arguments (dict): All the arguments for the function.

        Returns:
            str: The summarised results.
        """
        result: list[Document] = TavilySearchAPIRetriever(k=2).invoke(arguments["query"])
        return self.__summarise_results(query=arguments["query"], results=result)