import os
import chromadb
from openai import OpenAI

# --- API KEY GATEWAY RETRIEVAL ---
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key and os.path.exists(os.path.join(".streamlit", "secrets.toml")):
    try:
        with open(os.path.join(".streamlit", "secrets.toml"), "r", encoding="utf-8") as f:
            for line in f:
                if "OPENROUTER_API_KEY" in line and "=" in line:
                    api_key = line.split("=")[1].strip().strip('"').strip("'")
                    break
    except Exception as e:
        print(f"Note: Could not parse local secrets.toml file: {e}")

if not api_key:
    print("❌ Error: OPENROUTER_API_KEY is missing from environment/secrets.toml.")
    exit()

EMBEDDING_MODEL = "openai/text-embedding-3-small"
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def chunk_text(text, max_chars=300):
    """Splits a document cleanly by sentences or logical boundaries."""
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_db_embeddings():
    if not os.path.exists("core_policy.txt"):
        print("❌ Error: core_policy.txt not found in this working directory.")
        return

    with open("core_policy.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 1. Chunking Context Text Slices
    chunks = chunk_text(raw_text)
    print(f"✨ Generated {len(chunks)} structural context blocks.")

    # 2. Spin up Persistent Chroma DB Instance
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Reset/Recreate the storage space to prevent duplicate stacking data records
    try:
        chroma_client.delete_collection(name="swift_support_policy")
    except Exception:
        pass
        
    collection = chroma_client.get_or_create_collection(name="swift_support_policy")

    # 3. Vectorization & Database Registration Loop
    for i, chunk in enumerate(chunks):
        print(f"Vectorizing chunk {i+1}/{len(chunks)} into database index...")
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=chunk
            )
            embedding = response.data[0].embedding
            
            # Formally commit data record natively directly into the database engine
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[f"id_{i}"]
            )
        except Exception as e:
            print(f"❌ Failed to store index chunk {i}: {e}")
            return

    print("🚀 Success: ChromaDB vector collections compiled safely into ./chroma_db!")

if __name__ == "__main__":
    generate_db_embeddings()