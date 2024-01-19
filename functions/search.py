from Function import BaseFunction, Parameter, ParameterType, Property, PropertyType
from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever
from langchain.llms.ollama import Ollama
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

class SearchFunction(BaseFunction):
    def __init__(self, model: str):
        self.llm = Ollama(model=model)
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
        
    def __summarise_results(self, query: str, results: list) -> str:
        prompt_template = "Respond to the users query with a concise summary of the search results: \n users query: "+query+" \nsearch results: {results} \nCONCISE SUMMARY:"
        prompt = PromptTemplate.from_template(prompt_template)
        chain = StuffDocumentsChain(llm_chain=LLMChain(llm=self.llm, prompt=prompt), document_variable_name="results")
        return chain.run(results)
        
    def __call__(self, arguments: dict) -> str:
        result = TavilySearchAPIRetriever(k=2).invoke(arguments["query"])
        return self.__summarise_results(query=arguments["query"], results=result)