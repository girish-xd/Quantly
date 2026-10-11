import threading
import time
from typing import Optional
import pandas as pd

DEFAULT_SESSION_TTL_SECONDS = 3600  # 1 hour
DEFAULT_MAX_SESSIONS = 100


class SessionStore:
    """
    Thread-safe, bounded in-memory store for session expense DataFrames.

    LIMITATION & ARCHITECTURAL NOTICE:
    This store holds DataFrames in process-local memory. In a multi-worker
    production setup (e.g. Uvicorn/Gunicorn with 2+ worker processes), state
    is isolated per process and not shared across workers.
    For horizontal multi-worker scaling, external shared storage (such as
    Redis or shared object storage like S3/GCS with session mapping) is required.
    """

    def __init__(
        self,
        ttl_seconds: int = DEFAULT_SESSION_TTL_SECONDS,
        max_sessions: int = DEFAULT_MAX_SESSIONS,
    ):
        self._store: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._ttl_seconds = ttl_seconds
        self._max_sessions = max_sessions

    def _cleanup_expired_locked(self, current_time: float) -> None:
        """Evicts expired sessions under an existing lock."""
        expired_keys = [
            sid
            for sid, data in self._store.items()
            if current_time - data["updated_at"] > self._ttl_seconds
        ]
        for sid in expired_keys:
            del self._store[sid]

    def save_dataframe(self, session_id: str, df: pd.DataFrame) -> None:
        """Saves a pandas DataFrame with bounded capacity and TTL tracking."""
        with self._lock:
            now = time.time()
            self._cleanup_expired_locked(now)

            # Enforce bounded capacity via LRU-style eviction (oldest updated_at first)
            if len(self._store) >= self._max_sessions and session_id not in self._store:
                oldest_sid = min(
                    self._store.keys(), key=lambda k: self._store[k]["updated_at"]
                )
                del self._store[oldest_sid]

            self._store[session_id] = {
                "df": df,
                "updated_at": now,
            }

    def get_dataframe(self, session_id: str) -> Optional[pd.DataFrame]:
        """Retrieves DataFrame if session exists and is not expired."""
        with self._lock:
            now = time.time()
            entry = self._store.get(session_id)
            if entry is None:
                return None

            if now - entry["updated_at"] > self._ttl_seconds:
                del self._store[session_id]
                return None

            entry["updated_at"] = now
            return entry["df"]

    def remove_session(self, session_id: str) -> bool:
        """Removes a session DataFrame explicitly."""
        with self._lock:
            return self._store.pop(session_id, None) is not None

    def clear(self) -> None:
        """Clears all sessions (useful for test resets)."""
        with self._lock:
            self._store.clear()

    def count(self) -> int:
        """Returns the number of active unexpired sessions."""
        with self._lock:
            self._cleanup_expired_locked(time.time())
            return len(self._store)


# Global singleton instance maintaining backward compatibility
_session_store_instance = SessionStore()


def save_dataframe(session_id: str, df: pd.DataFrame) -> None:
    """Saves a pandas DataFrame to the global bounded session store."""
    _session_store_instance.save_dataframe(session_id, df)


def get_dataframe(session_id: str) -> Optional[pd.DataFrame]:
    """Retrieves the pandas DataFrame for a session ID, or None if not found or expired."""
    return _session_store_instance.get_dataframe(session_id)