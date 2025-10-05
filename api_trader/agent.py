# Third party imports
from dotenv import dotenv_values

# Default values
DEFAULT_ENV_FILE = "../.env"


class Agent:
    def __init__(self, env_filepath: str=DEFAULT_ENV_FILE):
        config = dotenv_values(env_filepath)
        self.api_key = config["api_key"]
        self.api_secret = config["secret"]