from Function import BaseFunction, Parameter, ParameterType, Property, PropertyType

class ChatFunction(BaseFunction):
    """
    A function derived from the BaseFunction class that allows the llm to respond to the user in a chat-like manner.

    Args:
        BaseFunction (_type_): The BaseFunction class to inherit from.
    """
    def __init__(self, personality: str = ""):
        """
        Instantiates a new ChatFunction object with the given personality.
        
        Example json function call:
        ```json
        {"name": "response_normal", "arguments": {"output": "Hello, how are you?"}}
        ```

        Args:
            personality (str, optional): The personality of the llm. Defaults to "".
        """
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
        """
        Returns the output from the arguments.

        Args:
            arguments (dict): All the arguments for the function.

        Returns:
            str: The output from the arguments.
        """
        return str(arguments["output"])