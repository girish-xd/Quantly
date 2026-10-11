from dotenv import load_dotenv
import os
import requests
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()

class StockNewsInput(BaseModel):
    query: str = Field(
        description="The stock ticker or company name to search news for. For example, 'TCS', 'Reliance', or 'AAPL'."
    )

@tool("get_stock_news", args_schema=StockNewsInput)
def get_stock_news(query: str) -> str:
    """Use this to get the latest news related to a stock or company. For example, you can query 'TCS' or 'Reliance'."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key or api_key.strip() == "":
        return "News service is currently unconfigured (NEWS_API_KEY is missing on the server)."

    clean_query = query.strip()
    try:
        req = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": clean_query,
                "apiKey": api_key,
                "pageSize": 5,
                "language": "en",
            },
            timeout=10,
        )

        data = req.json()
        if data.get("status") == "error":
            return f"News service error: {data.get('message', 'Failed to retrieve news.')}"

        articles = data.get("articles", [])
        if not articles:
            return f"No news found for '{clean_query}'."

        lines = []
        for i, article in enumerate(articles[:5]):
            title = article.get("title") or "No title"
            raw_date = article.get("publishedAt")
            date_str = f" (Published on {raw_date[:10]})" if raw_date and len(raw_date) >= 10 else ""
            desc = article.get("description") or "No description provided."
            lines.append(f"{i+1}. {title}{date_str}\n{desc}")

        return "\n\n".join(lines)
    except Exception as e:
        return f"Error fetching news for {clean_query}: {str(e)}"