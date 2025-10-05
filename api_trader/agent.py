# Standard library imports
from datetime import datetime

# Third party imports
from dotenv import dotenv_values

# Default values
DEFAULT_ENV_FILE = "../.env"


class Agent:
    def __init__(self, env_filepath: str=DEFAULT_ENV_FILE) -> None:
        config = dotenv_values(env_filepath)
        self.api_key = config["api_key"]
        self.api_secret = config["secret"]

        self.symbols = set()

    def set_symbols(self, symbols: list) -> None:
        self.symbols.update(symbols)

    def _get_data(self, start: datetime, end: datetime) -> None:
        pass

    def get_data(self, measure: str, amount: int, start_date: datetime) -> None:
        pass






if __name__ == "__main__":
    agent = Agent()
