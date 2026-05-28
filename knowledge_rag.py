import os
import chromadb
from openai import OpenAI

EMBEDDING_MODEL = "openai/text-embedding-3-small"
api_key = os.getenv("OPENROUTER_API_KEY")

# Safe initialization fallback for system routing
if not api_key and os.path.exists(os.path.join(".streamlit", "secrets.toml")):
    try:
        with open(os.path.join(".streamlit", "secrets.toml"), "r", encoding="utf-8") as f:
            for line in f:
                if "OPENROUTER_API_KEY" in line and "=" in line:
                    api_key = line.split("=")[1].strip().strip('"').strip("'")
                    break
    except Exception:
        pass

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key or "placeholder")

def retrieve_domain_context(user_query, top_k=1):
    """Vectorizes intent inputs and queries ChromaDB collection indexes directly."""
    db_path = "./chroma_db"
    
    # Safe fallback if database directory is empty or missing
    if not os.path.exists(db_path):
        if os.path.exists("core_policy.txt"):
            with open("core_policy.txt", "r", encoding="utf-8") as f:
                return f.read()
        return "Fulfillment policies are uninitialized."

    # 1. Connect to local database structure
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="swift_support_policy")

    # 2. Generate vector embedding for incoming search intent query
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=user_query
        )
        query_vector = response.data[0].embedding
    except Exception as e:
        print(f"RAG query embedding generation failed: {e}")
        return ""

    # 3. Natively query collection for nearest matches
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    # 4. Extract and return matching text blocks cleanly
    if results and 'documents' in results and len(results['documents'][0]) > 0:
        return "\n\n".join(results['documents'][0])
        
    return ""