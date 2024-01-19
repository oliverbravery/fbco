from Function import BaseFunction, Parameter, ParameterType, Property, PropertyType

class ChatFunction(BaseFunction):
    def __init__(self, personality: str = ""):
        super().__init__(name="response_normal", 
                         description="Respond to the user normally. If no other function is called, this function will be called.", 
                         parameters=[
                             Parameter(type=ParameterType.OBJECT,
                                        properties=[
                                             Property(name="output", 
                                                     type=PropertyType.STRING, 
                                                     attribute={'description': f'The response to the user. {personality}'}),
                                        ],
                                        required_parameters=["output"])
                         ])
        
    def __call__(self, arguments: dict) -> str:
        return str(arguments["output"])