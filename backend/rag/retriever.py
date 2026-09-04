import os
import json
from typing import List, Dict, Any
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

VECTOR_STORE_DIR = os.path.join("rag", "vector_store")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "bad_advice.index")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.json")
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class AdviceRetriever:
    def __init__(self):
        self.model = None
        self.index = None
        self.metadata: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
            return

        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(INDEX_PATH)
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    @property
    def is_ready(self) -> bool:
        return self.index is not None and len(self.metadata) > 0

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if not self.is_ready:
            return []

        query_vector = self.model.encode([query], convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, top_k)
        
        results: List[str] = []
        for idx in indices[0]:
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx]["advice"])
        return results


# Global singleton instance
retriever = AdviceRetriever()


def retrieve_terrible_advice(query: str, top_k: int = 3) -> List[str]:
    return retriever.search(query=query, top_k=top_k)