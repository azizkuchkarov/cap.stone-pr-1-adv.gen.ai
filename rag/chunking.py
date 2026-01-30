from typing import List
from .loaders import DocChunk

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    """
    Simple character-based chunking. Works well for capstone.
    You may replace with token-based chunking later.
    """
    text = " ".join(text.split())
    if len(text) <= chunk_size:
        return [text]

    out = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        out.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return out

def chunk_documents(pages: List[DocChunk], chunk_size: int = 900, overlap: int = 150) -> List[DocChunk]:
    final: List[DocChunk] = []
    for item in pages:
        pieces = chunk_text(item.text, chunk_size=chunk_size, overlap=overlap)
        for idx, p in enumerate(pieces):
            meta = dict(item.meta)
            meta["chunk_id"] = idx
            final.append(DocChunk(text=p, meta=meta))
    return final
