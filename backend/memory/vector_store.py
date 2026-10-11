import chromadb
import uuid
import os
from typing import List

BASE_DIR = os.path.dirname(__file__)
client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "../chroma_db"))

collection = client.get_or_create_collection(name="conversation_history")


def add_conversation(session_id: str, user_message: str, assistant_response: str) -> None:
    """
    Stores a conversation exchange in ChromaDB with session-scoped metadata.
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("A valid session_id is required to store conversation in memory.")

    combined_string = f"User: {user_message}\nAssistant: {assistant_response}"
    unique_id = str(uuid.uuid4())

    collection.add(
        documents=[combined_string],
        metadatas=[{"session_id": session_id}],
        ids=[unique_id],
    )


def query_conversations(session_id: str, query_text: str, n_results: int = 3) -> List[str]:
    """
    Queries ChromaDB strictly for conversations belonging to the specified session_id.
    Legacy unscoped records and other sessions are strictly filtered out.
    """
    if not session_id or not isinstance(session_id, str):
        return []

    if collection.count() == 0:
        return []

    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"session_id": session_id},
        )

        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            return [doc for doc in docs if isinstance(doc, str)]
        return []
    except Exception:
        # ChromaDB may raise if no documents match where criteria in certain versions
        return []