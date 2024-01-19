from Function import BaseFunction, Parameter, ParameterType, Property, PropertyType
from pyowm import OWM
from pyowm.weatherapi25.weather_manager import WeatherManager
import os

class WeatherFunction(BaseFunction):
    def __init__(self):
        self.weather_manager: WeatherManager = OWM(os.getenv("OWM_API_KEY")).weather_manager()
        super().__init__(name="get_current_weather", 
                         description="Should only be used for checking the weather or temperature for a given location.", 
                         parameters=[
                             Parameter(type=ParameterType.OBJECT,
                                        properties=[
                                             Property(name="location", 
                                                     type=PropertyType.STRING, 
                                                     attribute={'description': 'The city and Country, e.g. Newcastle Upon Tyne,Uk'}),
                                             Property(name="units",
                                                        type=PropertyType.STRING,
                                                        attribute={'enum': ["celsius", "fahrenheit"]})
                                        ],
                                        required_parameters=["location"])
                         ])
        
    def __call__(self, arguments: dict) -> str:
        weather = self.weather_manager.weather_at_place(arguments["location"]).weather
        temp = weather.temperature(arguments["units"])["temp"]
        return f'The temperature in {arguments["location"]} is {temp} degrees {arguments["units"]}.'