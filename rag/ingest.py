import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DATA_PATH = os.path.join("data", "bad_advice.json")
VECTOR_STORE_DIR = os.path.join("rag", "vector_store")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "bad_advice.index")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.json")
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def build_vector_store():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Cannot find {DATA_PATH}. Make sure Stage B3 is complete.")

    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    print(f"Loading data from {DATA_PATH}...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        advice_items = json.load(f)

    # Combine category, topic, and advice text for richer semantic indexing
    corpus_texts = [
        f"{item['category']} {item['topic']}: {item['advice']}"
        for item in advice_items
    ]

    print(f"Loading embedding model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    print(f"Encoding {len(corpus_texts)} bad advice items...")
    embeddings = model.encode(corpus_texts, convert_to_numpy=True, show_progress_bar=True)
    embeddings = embeddings.astype(np.float32)

    # Normalize vectors so Inner Product (IP) corresponds to Cosine Similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    print(f"Writing index to {INDEX_PATH}...")
    faiss.write_index(index, INDEX_PATH)

    print(f"Writing metadata to {METADATA_PATH}...")
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(advice_items, f, ensure_ascii=False, indent=2)

    print("RAG index creation finished successfully!")


if __name__ == "__main__":
    build_vector_store()