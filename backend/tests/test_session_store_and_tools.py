import time
import pandas as pd
from memory.session_store import SessionStore
from tools.analyze_expense import analyze_expenses
from tools.stock_news import get_stock_news
from utils.context import session_id_context


class TestSessionStore:
    def test_save_and_retrieve_dataframe(self):
        store = SessionStore(ttl_seconds=60, max_sessions=10)
        df = pd.DataFrame({"amount": [100, 200], "category": ["Food", "Rent"]})
        store.save_dataframe("sess_1", df)

        retrieved = store.get_dataframe("sess_1")
        assert retrieved is not None
        assert len(retrieved) == 2
        assert retrieved["amount"].tolist() == [100, 200]

    def test_session_store_ttl_expiration(self):
        store = SessionStore(ttl_seconds=1, max_sessions=10)
        df = pd.DataFrame({"amount": [50], "category": ["Fuel"]})
        store.save_dataframe("sess_exp", df)

        time.sleep(1.1)
        assert store.get_dataframe("sess_exp") is None

    def test_session_store_capacity_bound(self):
        store = SessionStore(ttl_seconds=60, max_sessions=2)
        df = pd.DataFrame({"amount": [10], "category": ["A"]})

        store.save_dataframe("s1", df)
        time.sleep(0.01)
        store.save_dataframe("s2", df)
        time.sleep(0.01)
        store.save_dataframe("s3", df)  # should evict oldest (s1)

        assert store.get_dataframe("s1") is None
        assert store.get_dataframe("s2") is not None
        assert store.get_dataframe("s3") is not None


class TestToolsHardening:
    def test_expense_analyzer_robust_parsing(self):
        from memory.session_store import save_dataframe
        test_sid = "test_robust_sess"

        # Dirty amounts with currency symbols, commas, spaces, and nulls
        df = pd.DataFrame({
            "Category": ["Groceries", "Rent", "Dining", "InvalidRow"],
            "Amount": ["$ 1,250.50", "₹ 25,000", "  45.00  ", "N/A"],
            "Description": ["Supermarket", "Apartment", "Dinner", "Unknown"]
        })
        save_dataframe(test_sid, df)

        session_id_context.set(test_sid)
        output = analyze_expenses.invoke({"query": "analyze my expenses"})

        assert "Total Expenses: 26295.5" in output
        assert "Breakdown by Category:" in output
        assert "- Rent: 25000.0" in output
        assert "- Groceries: 1250.5" in output


    def test_expense_analyzer_missing_columns(self):
        from memory.session_store import save_dataframe
        test_sid = "test_missing_cols"
        df = pd.DataFrame({"item": ["Laptop"], "cost": [1000]})
        save_dataframe(test_sid, df)

        session_id_context.set(test_sid)
        output = analyze_expenses.invoke({"query": "show spending"})
        assert "CSV must have 'amount' and 'category' columns." in output


    def test_stock_news_unconfigured_api_key(self, monkeypatch):
        monkeypatch.delenv("NEWS_API_KEY", raising=False)
        output = get_stock_news.invoke({"query": "TCS"})
        assert "News service is currently unconfigured" in output
