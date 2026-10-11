import yfinance as yf
from langchain.tools import tool
from pydantic import BaseModel, Field

class StockPriceInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol, e.g., AAPL, TCS.NS")

@tool("get_stock_price", args_schema=StockPriceInput)
def get_stock_price(ticker: str) -> str:
    """Use this to get the current stock price of a given ticker symbol.
    For Indian stocks use NSE suffix, e.g. 'TCS.NS', 'RELIANCE.NS'.
    For US stocks use the plain ticker, e.g. 'AAPL', 'GOOGL'."""
    clean_ticker = ticker.strip().upper()
    try:
        dat = yf.Ticker(clean_ticker)
        
        # 1. Try fast_info (faster and more reliable in modern yfinance)
        price = None
        currency = None
        try:
            fast = getattr(dat, "fast_info", None)
            if fast:
                price = getattr(fast, "last_price", None) or fast.get("lastPrice")
                currency = getattr(fast, "currency", None) or fast.get("currency")
        except Exception:
            pass

        # 2. Fallback to dat.info if fast_info didn't resolve price
        if price is None:
            try:
                info = dat.info or {}
                price = info.get("currentPrice") or info.get("regularMarketPrice")
                if not currency:
                    currency = info.get("currency")
            except Exception:
                pass

        if price is None:
            return f"Could not retrieve price information for {clean_ticker}. Please verify the ticker symbol."

        # Format currency representation cleanly
        curr_str = ""
        if currency:
            currency_upper = currency.upper()
            if currency_upper == "INR" or clean_ticker.endswith(".NS") or clean_ticker.endswith(".BO"):
                curr_str = "₹"
            elif currency_upper == "USD":
                curr_str = "$"
            elif currency_upper == "EUR":
                curr_str = "€"
            elif currency_upper == "GBP":
                curr_str = "£"
            else:
                curr_str = f"{currency_upper} "
        else:
            if clean_ticker.endswith(".NS") or clean_ticker.endswith(".BO"):
                curr_str = "₹"
            else:
                curr_str = "$"

        return f"{clean_ticker} is currently trading at {curr_str}{price:,.2f}"
    except Exception as e:
        return f"Error fetching price for {clean_ticker}: {str(e)}"