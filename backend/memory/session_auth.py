import hashlib
import hmac
import secrets
import threading
import time
from typing import Optional

DEFAULT_AUTH_TTL_SECONDS = 86400  # 24 hours
DEFAULT_MAX_AUTH_SESSIONS = 5000


class SessionAuthManager:
    """
    Manages server-issued anonymous session identities and cryptographically
    secure opaque bearer tokens.

    LIMITATIONS & THREAT MODEL:
    - Tokens are high-entropy, opaque strings generated via `secrets.token_urlsafe(32)` (256 bits).
    - Plaintext tokens are NEVER stored; only SHA-256 digests are maintained in memory.
    - Limits of anonymous sessions: Anonymous sessions authenticate session ownership,
      not personal user identities (no email/password or OAuth). Possession of the bearer token
      grants access to the specific session.
    - Token theft risk: If a token is compromised via client-side XSS, insecure transmission,
      or browser storage leakage, the session can be accessed until expiration.
    - Single-worker limitation: In-memory session tracking is process-local. A multi-worker
      deployment (e.g. Uvicorn with multiple workers or clustered containers) requires an
      external distributed store (e.g., Redis) or signed stateless JWT tokens with key rotation.
    """

    def __init__(
        self,
        ttl_seconds: int = DEFAULT_AUTH_TTL_SECONDS,
        max_sessions: int = DEFAULT_MAX_AUTH_SESSIONS,
    ):
        self._tokens: dict[str, dict] = {}  # token_hash -> {session_id, created_at, last_active}
        self._lock = threading.Lock()
        self._ttl_seconds = ttl_seconds
        self._max_sessions = max_sessions

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _cleanup_expired_locked(self, current_time: float) -> None:
        expired = [
            th for th, data in self._tokens.items()
            if current_time - data["last_active"] > self._ttl_seconds
        ]
        for th in expired:
            del self._tokens[th]

    def create_session(self) -> tuple[str, str]:
        """Issues a new session_id and a secure, high-entropy opaque bearer token."""
        session_id = secrets.token_hex(16)
        session_token = secrets.token_urlsafe(32)
        token_hash = self._hash_token(session_token)
        now = time.time()

        with self._lock:
            self._cleanup_expired_locked(now)
            if len(self._tokens) >= self._max_sessions:
                oldest = min(self._tokens.keys(), key=lambda k: self._tokens[k]["last_active"])
                del self._tokens[oldest]

            self._tokens[token_hash] = {
                "session_id": session_id,
                "created_at": now,
                "last_active": now,
            }

        return session_id, session_token

    def validate_session(self, session_id: str, session_token: Optional[str]) -> bool:
        """Validates that the provided session_token corresponds to the claimed session_id."""
        if not session_id or not session_token:
            return False

        token_hash = self._hash_token(session_token)
        now = time.time()

        with self._lock:
            data = self._tokens.get(token_hash)
            if data is None:
                return False

            if now - data["last_active"] > self._ttl_seconds:
                del self._tokens[token_hash]
                return False

            # Constant-time comparison to prevent timing attacks
            if not hmac.compare_digest(data["session_id"], session_id):
                return False

            data["last_active"] = now
            return True

    def revoke_session(self, session_token: str) -> bool:
        """Revokes a session by its token."""
        token_hash = self._hash_token(session_token)
        with self._lock:
            return self._tokens.pop(token_hash, None) is not None

    def clear(self) -> None:
        """Clears all sessions (useful for tests)."""
        with self._lock:
            self._tokens.clear()


auth_manager = SessionAuthManager()
