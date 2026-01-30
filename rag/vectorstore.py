import os
import pickle
from typing import List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from .loaders import DocChunk
from .config import settings

class FAISSStore:
    def __init__(self, embed_model_name: str = settings.EMBED_MODEL):
        self.embedder = SentenceTransformer(embed_model_name)
        self.index = None
        self.docstore: List[DocChunk] = []

    def _embed(self, texts: List[str]) -> np.ndarray:
        embs = self.embedder.encode(texts, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
        return embs.astype("float32")

    def build(self, chunks: List[DocChunk]):
        self.docstore = chunks
        vectors = self._embed([c.text for c in chunks])
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # cosine because normalized
        self.index.add(vectors)

    def save(self, index_path: str, docstore_path: str):
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(docstore_path, "wb") as f:
            pickle.dump(self.docstore, f)

    def load(self, index_path: str, docstore_path: str):
        self.index = faiss.read_index(index_path)
        with open(docstore_path, "rb") as f:
            self.docstore = pickle.load(f)

    def search(self, query: str, top_k: int) -> List[Tuple[DocChunk, float]]:
        qv = self._embed([query])
        scores, idxs = self.index.search(qv, top_k)
        results = []
        for i, score in zip(idxs[0], scores[0]):
            if i == -1:
                continue
            results.append((self.docstore[int(i)], float(score)))
        return results
