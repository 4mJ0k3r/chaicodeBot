# embeddings.py

import os
import json
from dotenv import load_dotenv

from vector_store import VectorStore

load_dotenv()  # so OPENAI_API_KEY & QDRANT_URL are in os.environ

def main():
    # 1. Read in all your chunks
    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks from disk.")

    # 2. Initialize your VectorStore (Qdrant + OpenAIEmbeddings)
    vs = VectorStore(api_key=os.getenv("OPENAI_API_KEY"))

    # 3. Add all chunks to Qdrant
    vs.add_chunks(chunks)
    print("✅ All chunks have been embedded and upserted into Qdrant.")

if __name__ == "__main__":
    main()
