import chromadb
import uuid
import os

BASE_DIR = os.path.dirname(__file__)
client = chromadb.PersistentClient(path = os.path.join(BASE_DIR, "../chroma_db"))

collection = client.get_or_create_collection(name = "conversation_history")

def add_conversation(user_message: str, assistant_response: str) -> None:
    """
    Combines a user message and assistant response, then stores it in ChromaDB
    with a unique UUID.
    """
    combined_string = f"User: {user_message}\nAssistant: {assistant_response}"
    unique_id = str(uuid.uuid4())

    collection.add(
        documents=[combined_string],
        ids=[unique_id]
    )

def query_conversations(query_text: str, n_results: int = 3) -> list:
    """
    Queries the conversation history for the closest semantic matches to the query_text.
    Returns a flat list of document strings.
    """
    results = collection.query(
        query_texts = [query_text],
        n_results = n_results
    )

    return results["documents"][0]