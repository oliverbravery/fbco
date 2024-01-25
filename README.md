# Function Based Chat Ollama (FBCO)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
Function Based Chat Ollama (FBCO) is a wrapper for the langchain OllamaFunctions class that allows for easy function creation and integration using the BaseFunction template. FBCO is designed to run locally on your machine using [Ollama](https://github.com/ollama/ollama). It is not yet recommended to use FBCO in a production environment.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements
This project has only been tested using Python 3.11. It is recommended to use this version of Python to avoid any compatibility issues.

[ChatOllamaFunctions](ChatOllamaFunctions.py) class is build ontop of the [langchain OllamaFunctions class](https://python.langchain.com/docs/get_started/quickstart). All models are run through Ollama. For more information and installation instructions on Ollama, please visit the [Ollama GitHub](https://github.com/ollama/ollama).


## Installation
To install FBCO, first clone this repository to your local machine. 

Next create a virtual python environment and install the requirements using pip.
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Next copy the [.env.template](.env.template) file and rename it to .env. Fill in the values for the environment variables.
```bash
cp .env.template .env
```
Finally, run the main.py file to test the installation.
```bash
python main.py
```

Please note that Ollama must be open in the background for the program to run. The first time you run the main.py file, it may take a while to download the Ollama models. This is normal and will only happen once.

## Usage
### ChatOllamaFunctions
To use FBCO in other project import the ChatOllamaFunctions class from the [ChatOllamaFunctions.py](ChatOllamaFunctions.py) file.
```python
from ChatOllamaFunctions import ChatOllamaFunctions
```
Next create an instance of the ChatOllamaFunctions class. The `functions` parameter should be a list of functions that inherit from the BaseFunction class.
```python
chat_llm: ChatOllamaFunctions = ChatOllamaFunctions(
    functions=[...], 
    model='dolphin-mistral')
```
To query the llm use the `run` function.
```python
chat_llm.run(input='Hello llm, how are you?')
```
More examples can be found in the [main.py](main.py) file.

### Creating custom functions
To create a custom function to use with the llm, first create a class that inherits from the BaseFunction class. The BaseFunction class is located in the [BaseFunction.py](BaseFunction.py) file. The constructor should be overriden and the BaseFunction's constructor should be called. 

The BaseFunction constructor requires the name of the function and the function's description so the llm knows what use the function has and also the parameters of the function. Please refer to the functions already created in the [functions](functions) folder for examples.

The `__call__` function should also be overriden. This function is called when the function is called by the llm. It should contain the logic for the function and return a string that will be used as the response from the llm.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please note that this project is not actively maintained and pull requests may take a while to be reviewed.

## License
This project is licensed under the terms of the [MIT](LICENSE) license.