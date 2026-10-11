from langchain_groq import ChatGroq
from dotenv import load_dotenv
# from langchain.agents import AgentExecutor
# from langchain.agents.react.agent import create_react
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from tools.analyze_expense import analyze_expenses
from tools.budget_calculator import budget_calculator
from tools.market_summary import get_market_summary
from tools.stock_news import get_stock_news
from tools.stock_price import get_stock_price

from memory.rag import get_relevant_context
from memory.vector_store import add_conversation

load_dotenv()

def build_agent(context: str = ""):
    # llm = ChatGroq(model = "llama-3.3-70b-versatile")
    llm = ChatGroq(model="llama-3.1-8b-instant")
    tool_list = [analyze_expenses, budget_calculator, get_market_summary, get_stock_news, get_stock_price]

    base_instructions = "You are an expert financial analyst. Provide clear, accurate, and concise answers."

    if context:
        final_instructions = f"{context}\n\n{base_instructions}"
    else:
        final_instructions = base_instructions

    agent = create_agent(
        model = llm,
        tools = tool_list,
        system_prompt = SystemMessage(content = final_instructions)
    )

    return agent

from utils.context import session_id_context
from typing import Optional


def run_agent(user_input: str, session_id: Optional[str] = None) -> str:
    active_session_id = session_id or session_id_context.get(None)

    context = get_relevant_context(active_session_id, user_input) if active_session_id else ""

    agent_graph = build_agent(context)

    res = agent_graph.invoke({"messages": [("user", user_input)]})
    response_text = res["messages"][-1].content

    if active_session_id:
        add_conversation(active_session_id, user_input, response_text)

    return response_text


# print(run_agent("What is the stock price of AAPL?"))
# """You are an expert financial analyst. 
    
#     Before calling any tool, you must explicitly write out your reasoning 
#     step-by-step. Explain what data you need, why you need it, and which 
#     tool you will use to get it."""

# """You are an expert financial analyst. 
    
#     You have access to several financial tools. If a user asks a question 
#     that requires real-time data or calculations, use the appropriate tool. 
    
#     If the user asks a general knowledge question or something you can answer 
#     directly without a tool, just answer them directly. Do not use tools 
#     unnecessarily."""