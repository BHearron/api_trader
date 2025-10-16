# Standard library imports
from datetime import datetime
from datetime import timedelta

# Third party imports
import pandas
from dotenv import dotenv_values
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockTradesRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

# Default values
DEFAULT_ENV_FILE = ".env"


class Agent:
    def __init__(self, env_filepath: str=DEFAULT_ENV_FILE) -> None:
        config = dotenv_values(env_filepath)
        self.api_key = config["api_key"]
        self.api_secret = config["secret"]

        self.historical_client = StockHistoricalDataClient(
            self.api_key,
            self.api_secret
        )

        self.symbols = set()

    def set_symbols(self, symbols: list) -> None:
        self.symbols.update(symbols)

    def _get_trades(self, start: datetime, end: datetime) -> pandas.DataFrame:
        request_params = StockTradesRequest(
            symbol_or_symbols=list(self.symbols),
            start=start,
            end=end,
            timeframe=TimeFrame.Minute
        )
        trades = self.historical_client.get_stock_trades(request_params)
        
        stock_table = {
            "symbol": [],
            "timestamp": [],
            "price": [],
            "size": [],
            "id": [],
            "conditions": [],
            "tape": []
        }
        for stock_name in trades.data:
            for item in trades.data[stock_name]:
                stock_table["symbol"].append(item.symbol)
                stock_table["timestamp"].append(item.timestamp)
                stock_table["price"].append(item.price)
                stock_table["size"].append(item.size)
                stock_table["id"].append(item.id)
                stock_table["conditions"].append(item.conditions)
                stock_table["tape"].append(item.tape)
        stock_table = pandas.DataFrame(stock_table)

        return stock_table

    def get_trades(self, measure: str, amount: int, end_date: datetime=datetime.now()) -> pandas.DataFrame:
        start_date = end_date
        match measure:
            case "minutes":
                start_date -= timedelta(minutes=amount) 
            case "hours":
                start_date -= timedelta(hours=amount)
            case "days":
                start_date -= timedelta(days=amount)

        return self._get_trades(start_date, end_date)
    

    def _get_data(
            self, symbols: list[str], timeframe: TimeFrame, 
            start_date: datetime=None, end_date: datetime=datetime.now()
        ) -> pandas.DataFrame:
        request = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start_date,
            end=end_date
        )
        bars_data = self.historical_client.get_stock_bars(request)
        print(bars_data)



if __name__ == "__main__":
    # Set parameters for testing
    symbols = ['AAPL', "TSLA"]
    start_date = "2025-10-15 10:00AM"
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M%p")
    
    agent = Agent()
    agent.set_symbols(symbols)  # depricated

    agent._get_data(
        symbols = symbols, 
        timeframe = TimeFrame(5, TimeFrameUnit.Minute),
        start_date = start_date
    )