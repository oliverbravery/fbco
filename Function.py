from enum import Enum

class PropertyType(Enum):
    STRING = 'string'
    NUMBER = 'number'
    BOOLEAN = 'boolean'
    ARRAY = 'array'
    
class ParameterType(Enum):
    OBJECT = 'object'
    
class Property:
    def __init__(self, name: str, type: PropertyType, attribute: dict):
        self.name: str = name
        self.type: PropertyType = type
        self.attribute: dict = attribute
        
    def __dict__(self):
        return {self.name: {
            'type': self.type.value,
            **self.attribute
        }}
        
class Parameter:
    def __init__(self, type: ParameterType, properties: list[Property], required_parameters: list[str]):
        self.properties: list[Property] = properties
        self.type: ParameterType = type
        self.required_parameters: list[str] = required_parameters
        
    def __dict__(self):
        return {
            'properties': [property.__dict__() for property in self.properties],
            'type': self.type.value,
            'required_parameters': self.required_parameters
        }
        
class BaseFunction:
    def __init__(self, name: str, description: str, parameters: list[Parameter]):
        self.name = name
        self.description = description
        self.parameters = parameters

    def __dict__(self):
        return {
            'name': self.name,
            'description': self.description,
            'parameters': [parameter.__dict__() for parameter in self.parameters]
        }
        
    def __call__(self, *args, **kwargs) -> any:
        return None
        
def json_to_function(func_json: dict) -> BaseFunction:
    return BaseFunction(**func_json)

def json_to_functions(func_json: dict) -> list[BaseFunction]:
    return [BaseFunction(**func_json) for func_json in func_json["functions"]]

def functions_to_json(funcs: list[BaseFunction]) -> list[dict]:
    return [func.__dict__() for func in funcs]