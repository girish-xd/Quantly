import yfinance as yf
from langchain.tools import tool
from pydantic import BaseModel, Field

class StockPriceInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol, e.g., AAPL")

@tool("get_stock_price", args_schema=StockPriceInput)
def get_stock_price(ticker: str) -> str:
    """Use this to get the current stock price of a given ticker symbol.
    For Indian stocks use NSE suffix, e.g. 'TCS.NS', 'RELIANCE.NS'.
    For US stocks use the plain ticker, e.g. 'AAPL', 'GOOGL'."""
    try:
        dat = yf.Ticker(ticker)
        price = dat.info.get('currentPrice')
        if price is None:
            return f"Could not retrieve price information for {ticker}"
        return f"{ticker} is currently trading at ${price}"
    except Exception as e:
        return f"Error fetching price for {ticker}: {str(e)}"