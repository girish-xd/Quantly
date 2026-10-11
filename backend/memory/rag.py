from memory.vector_store import query_conversations
from typing import Optional


def get_relevant_context(session_id: Optional[str], user_message: str) -> str:
    """
    Retrieves semantically similar past conversations from ChromaDB 
    scoped strictly to the given session_id, and formats them into
    a single string context block.
    """
    if not session_id:
        return ""

    res = query_conversations(session_id, user_message)

    if not res:
        return ""

    valid_docs = [doc for doc in res if doc and isinstance(doc, str)]
    if not valid_docs:
        return ""

    joined_results = "\n---\n".join(valid_docs)

    return f"Relevant past conversations:\n{joined_results}"

