import pandas as pd
from typing import Optional

# Single shared instance across imports
session_store: dict = {}


def save_dataframe(session_id: str, df: pd.DataFrame) -> None:
    """Saves a pandas DataFrame to the global session store."""
    session_store[session_id] = df


def get_dataframe(session_id: str) -> Optional[pd.DataFrame]:
    """Retrieves the pandas DataFrame for a session ID, or None if not found."""
    return session_store.get(session_id)