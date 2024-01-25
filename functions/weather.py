from Function import BaseFunction, Parameter, ParameterType, Property, PropertyType
from pyowm import OWM
from pyowm.weatherapi25.weather_manager import WeatherManager
from pyowm.weatherapi25.weather import Weather
import os

class WeatherFunction(BaseFunction):
    """
    A function derived from the BaseFunction class that allows the llm to get the current weather for a given location.

    Args:
        BaseFunction (_type_): The BaseFunction class to inherit from.
    """
    def __init__(self, owm_api_key: str = os.getenv("OWM_API_KEY")):
        """
        A function derived from the BaseFunction class that allows the llm to get the current weather for a given location.

        Example json function call:
        ```json
        {"name": "get_current_weather", "arguments": {"location": "London,Uk", "units": "celsius"}}
        ```

        Args:
            owm_api_key (str, optional): The OWM API key. Defaults to "OWM_API_KEY" environmental variable.
        """
        self.weather_manager: WeatherManager = OWM(owm_api_key).weather_manager()
        super().__init__(name="get_current_weather", 
                         description="Should only be used for checking the weather or temperature for a given location.", 
                         parameters=[
                             Parameter(type=ParameterType.OBJECT,
                                        properties=[
                                             Property(name="location", 
                                                     type=PropertyType.STRING, 
                                                     attribute={'description': 'The city and Country, e.g. London,Uk'}),
                                             Property(name="units",
                                                        type=PropertyType.STRING,
                                                        attribute={'enum': ["celsius", "fahrenheit"]})
                                        ],
                                        required_parameters=["location"])
                         ])
        
    def __call__(self, arguments: dict) -> str:
        """
        Returns the current temperature for the given location in a formatted string.

        Args:
            arguments (dict): All the arguments for the function.

        Returns:
            str: The current temperature for the given location in a formatted string.
        """
        weather: Weather = self.weather_manager.weather_at_place(arguments["location"]).weather
        temp: str = weather.temperature(arguments["units"])["temp"]
        return f'The temperature in {arguments["location"]} is {temp} degrees {arguments["units"]}.'