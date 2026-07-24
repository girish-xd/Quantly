from contextvars import ContextVar

# Thread-safe, async-safe storage for the current request's session ID
session_id_context: ContextVar[str] = ContextVar("session_id")