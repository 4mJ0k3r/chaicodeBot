# vector_store.py

import os
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

class VectorStore:
    def __init__(self, api_key: str):
        # 1. Init OpenAI embeddings (text-embedding-3-large)
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            openai_api_key=api_key
        )

        # 2. Connect to Qdrant: either memory or your Docker URL
        qdrant_url = os.getenv("QDRANT_URL")
        if qdrant_url:
            self.client = QdrantClient(url=qdrant_url, prefer_grpc=True)
        else:
            self.client = QdrantClient(":memory:")
        
        # 3. Ensure collection exists
        collection_name = "chai_docs"
        if not self.client.collection_exists(collection_name):
            # text-embedding-3-large has 3072 dimensions
            embedding_size = 3072
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=embedding_size,
                    distance=Distance.COSINE
                )
            )

        # 4. Wrap it in LangChain’s store
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embeddings
        )

    def add_chunks(self, chunks: List[Dict]):
        # Extract texts + metadata, then upsert in batch
        texts = [chunk["content"] for chunk in chunks]
        metadatas = [
            {k: v for k, v in chunk.items() if k != "content"}
            for chunk in chunks
        ]
        self.vector_store.add_texts(texts=texts, metadatas=metadatas)

    def search(self, query: str, k: int = 3) -> List[Dict]:
        # Return top-k similar chunks, plus scores
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            }
            for doc, score in results
        ]
