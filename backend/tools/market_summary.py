from pydantic import BaseModel
from langchain.tools import tool
import yfinance as yf

class EmptyInput(BaseModel):
    pass

@tool("get_market_summary", args_schema=EmptyInput)
def get_market_summary() -> str:
    """Use this to get a quick summary of the current market status. It will return the current price of major indices like Nifty 50, Sensex, S&P 500 and Nasdaq."""
    tickers = ["^NSEI", "^BSESN", "^GSPC", "^IXIC"]
    indices = {
        "^NSEI": "Nifty 50",
        "^BSESN": "Sensex",
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ"
    }
    summ_str = "Market Summary:\n"
    for ticker in tickers:
        try:
            dat = yf.Ticker(ticker)
            currPrice = dat.info.get('regularMarketPrice')
            summ_str += f"{indices.get(ticker)}: {currPrice}\n"
        except Exception as e:
            summ_str += f"{indices.get(ticker)}: Error fetching price\n"
    return summ_str

# print(get_market_summary())