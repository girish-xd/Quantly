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
    try:
        req = requests.get("https://newsapi.org/v2/everything", params={
            "q": query,
            "apiKey": os.getenv("NEWS_API_KEY"),
            "pageSize": 5,
            "language": "en"
        })
        # Pull the top 5 articles from the response; we just need the title, date publised and description
        string = ""
        articles = req.json().get("articles", [])
        if not articles:
            return f"No news found for {query}"
        for i, article in enumerate(articles[:5]):
            string += f"{i+1}. {article['title']} (Published on {article['publishedAt'][:10]})\n{article['description']}\n"

        return string
    except Exception as e:
        return f"Error fetching news for {query}: {str(e)}"