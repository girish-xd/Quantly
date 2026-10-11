import pytest
import uuid
import time
from memory.vector_store import add_conversation, query_conversations, collection
from memory.rag import get_relevant_context
from memory.session_auth import SessionAuthManager


class TestMemoryIsolation:
    def test_session_isolation_in_vector_store(self):
        """Proves that Session A cannot retrieve Session B's vector memories."""
        session_a = f"session_a_{uuid.uuid4()}"
        session_b = f"session_b_{uuid.uuid4()}"

        # Session A discusses private debt and salary
        add_conversation(
            session_a,
            "My secret salary is 150000 and debt is 40000",
            "I noted your salary is 150k and debt is 40k.",
        )

        # Session B discusses general investments
        add_conversation(
            session_b,
            "What is the best index fund to buy?",
            "Nifty 50 or S&P 500 index funds are great options.",
        )

        # Session A querying should see Session A's context
        results_a = query_conversations(session_a, "salary and debt", n_results=5)
        assert len(results_a) > 0
        assert any("150000" in doc for doc in results_a)
        assert not any("index fund" in doc for doc in results_a)

        # Session B querying for debt must NOT retrieve Session A's private debt context
        results_b = query_conversations(session_b, "salary and debt", n_results=5)
        assert not any("150000" in doc for doc in results_b)
        assert not any("40000" in doc for doc in results_b)

    def test_legacy_unscoped_records_never_leaked(self):
        """Proves that legacy records stored without session metadata are never returned to any new session."""
        legacy_id = f"legacy_{uuid.uuid4()}"
        # Insert a simulated legacy document with no metadata
        collection.add(
            documents=["User: Legacy secret data\nAssistant: Stored without metadata"],
            ids=[legacy_id],
        )

        new_session = f"session_clean_{uuid.uuid4()}"
        results = query_conversations(new_session, "Legacy secret data", n_results=5)
        assert not any("Legacy secret data" in doc for doc in results)

    def test_add_conversation_requires_session_id(self):
        """Proves that add_conversation rejects missing or empty session_id."""
        with pytest.raises(ValueError):
            add_conversation("", "Hello", "Hi")

        with pytest.raises(ValueError):
            add_conversation(None, "Hello", "Hi")

    def test_rag_context_is_session_scoped(self):
        """Proves get_relevant_context returns context only for the matching session."""
        session_x = f"session_x_{uuid.uuid4()}"
        session_y = f"session_y_{uuid.uuid4()}"

        add_conversation(session_x, "I live in Mumbai and work at TCS", "Noted your TCS role.")

        context_x = get_relevant_context(session_x, "Where do I work?")
        assert "TCS" in context_x

        context_y = get_relevant_context(session_y, "Where do I work?")
        assert context_y == ""


class TestSessionAuthManager:
    def test_create_and_validate_session(self):
        mgr = SessionAuthManager(ttl_seconds=60)
        session_id, session_token = mgr.create_session()

        assert session_id is not None and len(session_id) >= 16
        assert session_token is not None and len(session_token) >= 32

        # Valid credentials must succeed
        assert mgr.validate_session(session_id, session_token) is True

    def test_reject_spoofed_or_invalid_tokens(self):
        mgr = SessionAuthManager(ttl_seconds=60)
        session_id, session_token = mgr.create_session()

        # Spoofed session ID with real token
        assert mgr.validate_session("wrong_session_id", session_token) is False

        # Real session ID with fake token
        assert mgr.validate_session(session_id, "fake_token_12345678901234567890") is False

        # Missing token
        assert mgr.validate_session(session_id, None) is False
        assert mgr.validate_session(session_id, "") is False

    def test_expired_token_rejection(self):
        mgr = SessionAuthManager(ttl_seconds=1)
        session_id, session_token = mgr.create_session()

        # Fast forward time
        time.sleep(1.1)

        # Expired token must be rejected
        assert mgr.validate_session(session_id, session_token) is False
