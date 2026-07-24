from memory.vector_store import query_conversations

def get_relevant_context(user_message: str) -> str:
    """
    Retrieves semantically similar past conversations from ChromaDB 
    and formats them into a single string context block.
    """
    res = query_conversations(user_message)

    if not res:
        return ""
    
    joined_results = "\n---\n".join(doc for doc in res)

    return f"Relevant past conversations:\n{joined_results}"
