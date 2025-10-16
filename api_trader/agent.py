# Standard library imports
from datetime import datetime, timedelta

# Third party imports
import pandas
from dotenv import dotenv_values
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockTradesRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.models.bars import BarSet
from matplotlib import pyplot as plt

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
        ) -> BarSet:
        request = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start_date,
            end=end_date
        )
        data = self.historical_client.get_stock_bars(request)
        return data

    def get_data(
            self, symbols: list[str], timeframe: TimeFrame=TimeFrame(1, TimeFrameUnit.Minute), 
            start_date: datetime=None, end_date: datetime=datetime.now()
        ) -> pandas.DataFrame:
        data = self._get_data(symbols, timeframe, start_date, end_date)
        
        dataframe = {
            "symbol": [],
            "timestamp": [],
            "open": [],
            "close": [],
            "volume": [],
            "trades": [],
        }
        for symbol in symbols:
            symbol_data = data[symbol]
            for d in symbol_data:
                dataframe["symbol"].append(d.symbol)
                dataframe["timestamp"].append(d.timestamp)
                dataframe["open"].append(d.open)
                dataframe["close"].append(d.close)
                dataframe["volume"].append(d.volume)
                dataframe["trades"].append(d.trade_count)
        return pandas.DataFrame(dataframe)
    
    
    def test_strategy(self, data: pandas.DataFrame):
        money = 100

        # Ensure the table is sorted by timestamp
        # Iterate through each row on the table
        # If choose to buy, then subtract
        # If choose to sell then add 
        # Maybe add a toggle to switch from open/close for buy and sell?

        # Make a table with known trades. Essentially move the row from the starting
        # data table to a new table after iterated over. Can be used for strategy



if __name__ == "__main__":
    # Set parameters for testing
    symbols = ['AAPL']
    start_date = "2025-10-15 10:00AM"
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M%p")
    end_date = start_date + timedelta(minutes=5)

    # Test Agent
    agent = Agent()
    agent.get_data(
        symbols = symbols, 
        start_date = start_date,
        end_date = end_date
    )