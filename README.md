# 🚀 Quantly — Personal Finance AI Agent

Quantly is an AI-powered Personal Finance Assistant that combines real-time market intelligence, expense analysis, budgeting capabilities, and conversational financial guidance into a single intelligent agent.

Built using a modern React frontend and a LangGraph-powered ReAct AI agent, Quantly enables users to interact naturally with their finances through a chat-based interface while leveraging live market data, news feeds, and expense analytics.

---

## ✨ Features

### 🤖 AI Financial Assistant

* Natural language financial conversations
* Multi-turn contextual chat
* ReAct-based reasoning and tool calling
* Session-aware interactions

### 🧠 Memory & Context

* Short-term conversational memory
* Long-term memory using ChromaDB
* Retrieval-Augmented Generation (RAG)
* Personalized interactions across conversations

### 📊 Expense Analysis

* Upload expense CSV files directly
* AI-powered spending pattern analysis
* Category-wise expense breakdown
* Financial insights and recommendations

### 💰 Budget Planning

* Calculate remaining budget
* Analyze spending across categories
* Track budget utilization
* Generate actionable financial recommendations

### 📈 Live Market Intelligence

* Real-time stock prices
* Latest stock-related news
* Global and Indian market summaries
* Support for NSE, BSE, and international stocks

### 🎨 Modern User Experience

* Clean responsive UI
* Real-time thinking indicator
* Markdown-rendered responses
* Smooth animations powered by Framer Motion

---

## 🏗️ Architecture Overview

```text
┌─────────────────────────────────────┐
│            React Frontend           │
│   TypeScript + Vite + Tailwind v4   │
└──────────────────┬──────────────────┘
                   │
                   │ HTTP (Axios)
                   ▼
┌─────────────────────────────────────┐
│            FastAPI Backend          │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│      LangGraph ReAct AI Agent       │
└──────────────────┬──────────────────┘
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 ChromaDB      Groq LLM      Tools
  Memory      Qwen3-32B      Layer
                   │
                   ▼
        Financial Data Sources
```

---

## 🛠️ Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS v4
* Framer Motion
* Recharts
* Axios

### Backend

* FastAPI
* LangGraph
* ReAct Agent Architecture
* Groq API
* Qwen/Qwen3-32B
* ChromaDB

### Data Sources

* Yahoo Finance (yfinance)
* NewsAPI

---

## 🔧 Agent Tools

The AI agent can dynamically invoke the following tools during conversations:

### 1. get_stock_price

Fetches live stock prices from:

* NSE (National Stock Exchange)
* BSE (Bombay Stock Exchange)
* Global markets

**Example Queries**

```text
What is the current price of TCS?
Show me Apple stock price.
```

---

### 2. get_stock_news

Retrieves the latest news related to a stock using NewsAPI.

**Example Queries**

```text
What's happening with Tesla today?
Show recent news about Reliance.
```

---

### 3. analyze_expenses

Analyzes uploaded CSV expense files and generates insights.

Capabilities:

* Spending analysis
* Category identification
* Expense trends
* Financial recommendations

**Example Queries**

```text
Analyze my expenses.
Where am I overspending?
```

---

### 4. budget_calculator

Calculates:

* Remaining budget
* Category-wise allocation
* Spending summaries

**Example Queries**

```text
I have a monthly budget of ₹50,000.
How much do I have left?
```

---

### 5. get_market_summary

Provides a live overview of major indices:

* Nifty 50
* Sensex
* S&P 500
* NASDAQ

**Example Queries**

```text
Give me today's market summary.
How are global markets performing?
```

---

## 📁 Project Structure

```text
Quantly/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   └── services/
│
├── backend/
│   ├── agent/
│   ├── tools/
│   ├── routes/
│   ├── memory/
│   ├── chroma_db/
│   └── main.py
│
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file inside the backend directory.

```env
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_newsapi_key
```

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/quantly.git

cd quantly
```

---

### 2. Backend Setup

```bash
cd backend

python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI server:

```bash
uvicorn main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

---

### 3. Frontend Setup

```bash
cd frontend

npm install
```

Start development server:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

## 🔄 How It Works

1. User starts a chat session.
2. A unique Session ID is created.
3. Messages are sent to the FastAPI backend.
4. LangGraph orchestrates reasoning and tool selection.
5. The ReAct agent invokes tools when needed.
6. ChromaDB stores and retrieves relevant context.
7. Responses are streamed back to the frontend.
8. Chat history and memory improve future interactions.

---

## 🧠 Memory System

Quantly uses a hybrid memory architecture:

### Short-Term Memory

Maintains conversational context within an active session.

### Long-Term Memory

Stores relevant user interactions inside ChromaDB to enable:

* Context retention
* Personalized responses
* Better financial recommendations
* Retrieval-Augmented Generation (RAG)

---

## 📸 Key Capabilities

✅ Conversational Personal Finance Assistant

✅ Live Stock Market Data

✅ Financial News Aggregation

✅ Budget Planning

✅ Expense Analysis from CSV Uploads

✅ Long-Term Memory with ChromaDB

✅ LangGraph ReAct Agent

✅ Session-Based Architecture

✅ Responsive Modern UI

---

## 🎯 Why This Project?

Quantly demonstrates the integration of modern AI agent architectures with real-world financial workflows. The project showcases:

* Agentic AI Systems
* Tool Calling
* Retrieval-Augmented Generation (RAG)
* Memory Management
* FastAPI Backend Development
* Modern React Frontend Engineering
* Real-Time Financial Data Integration

It serves as a strong portfolio project highlighting full-stack development, AI engineering, and production-oriented system design.

---

## 📜 License

This project is intended for educational, learning, and portfolio purposes.

---

---

<div align="center">

## 🤖 Built by Girish Jain

Making personal finance smarter with AI, RAG, and real-time market intelligence.

From stock insights to budget planning — your financial copilot is just one prompt away.

⭐ Don't forget to star the repository.

</div>

---
