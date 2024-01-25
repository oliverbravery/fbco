from enum import Enum

class PropertyType(Enum):
    """
    PropertyType is an enumeration of the different types of properties that can be used in a function.
    """
    STRING = 'string'
    NUMBER = 'number'
    BOOLEAN = 'boolean'
    LIST = 'list'
    
class ParameterType(Enum):
    """
    ParameterType is an enumeration of the different types of parameters that can be used in a function.
    """
    OBJECT = 'object'
    
class Property:
    """
    Property is a class that represents a property that can be used in a function.
    """
    def __init__(self, name: str, type: PropertyType, attribute: dict):
        """
        Instantiates a new Property object with the given name, type and attribute.
        Args:
            name (str): The name of the property.
            type (PropertyType): The type of the property.
            attribute (dict): The attribute of the property.
        """
        self.name: str = name
        self.type: PropertyType = type
        self.attribute: dict = attribute
        
    def __dict__(self) -> dict:
        """
        Returns the Property object as a dictionary.
        Returns:
            dict: The Property object as a dictionary.
        """
        return {self.name: {
            'type': self.type.value,
            **self.attribute
        }}
        
class Parameter:
    """
    Parameter is a class that represents a parameter that can be used in a function.
    """
    def __init__(self, type: ParameterType, properties: list[Property], required_parameters: list[str]):
        """
        Instantiates a new Parameter object with the given type, properties and required_parameters.
        Args:
            type (ParameterType): The type of the parameter.
            properties (list[Property]): The properties of the parameter.
            required_parameters (list[str]): The names of parameters that are mandatory.
        """
        self.properties: list[Property] = properties
        self.type: ParameterType = type
        self.required_parameters: list[str] = required_parameters
        
    def __dict__(self) -> dict:
        """
        Returns the Parameter object as a dictionary.
        Returns:
            dict: The Parameter object as a dictionary.
        """
        return {
            'properties': [property.__dict__() for property in self.properties],
            'type': self.type.value,
            'required_parameters': self.required_parameters
        }
        
class BaseFunction:
    """
    BaseFunction is a class that represents a function used by the ChatOllamaFunctions class.
    """
    def __init__(self, name: str, description: str, parameters: list[Parameter]):
        """
        Instantiates a new BaseFunction object with the given name, description and parameters.
        Args:
            name (str): The name of the function.
            description (str): The description of the function for the llm.
            parameters (list[Parameter]): The parameters for the function.
        """
        self.name = name
        self.description = description
        self.parameters = parameters

    def __dict__(self) -> dict:
        """
        Returns the BaseFunction object as a dictionary.
        Returns:
            dict: The BaseFunction object as a dictionary.
        """
        return {
            'name': self.name,
            'description': self.description,
            'parameters': [parameter.__dict__() for parameter in self.parameters]
        }
        
    def __call__(self, *args, **kwargs) -> any:
        """
        The __call__ method is called when the llm chooses to invoke the function.
        This function should contain the logic to be called if this function is selected 
        by the llm. Override this method in your derived function's class.
        Returns:
            any: The value returned to the llm after the function has been invoked.
        """
        return None
        
def json_to_function(func_json: dict) -> BaseFunction:
    """
    json_to_function is a function that converts a json object into a BaseFunction object.
    Args:
        func_json (dict): The json object to convert.

    Returns:
        BaseFunction: The BaseFunction object instantiated from the json object.
    """
    return BaseFunction(**func_json)

def json_to_functions(func_json: dict) -> list[BaseFunction]:
    """
    json_to_functions is a function that converts a json object into a list of BaseFunction objects.
    Args:
        func_json (dict): The json object to convert.

    Returns:
        list[BaseFunction]: The list of BaseFunction objects instantiated from the json object.
    """
    return [BaseFunction(**func_json) for func_json in func_json["functions"]]

def functions_to_json(funcs: list[BaseFunction]) -> list[dict]:
    """
    functions_to_json is a function that converts a list of BaseFunction objects into a list of json objects.
    Args:
        funcs (list[BaseFunction]): The list of BaseFunction objects to convert.

    Returns:
        list[dict]: The list of json objects instantiated from the list of BaseFunction objects.
    """
    return [func.__dict__() for func in funcs]