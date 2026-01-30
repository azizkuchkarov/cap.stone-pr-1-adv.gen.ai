import os
import fitz  # PyMuPDF
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class DocChunk:
    text: str
    meta: Dict[str, Any]

def load_pdf(path: str) -> List[DocChunk]:
    """
    Loads PDF into page-level items (later chunked).
    meta includes: source, page
    """
    doc = fitz.open(path)
    out: List[DocChunk] = []
    basename = os.path.basename(path)

    for i in range(len(doc)):
        page = doc[i]
        text = page.get_text("text") or ""
        text = text.strip()
        if not text:
            continue
        out.append(DocChunk(
            text=text,
            meta={"source": basename, "page": i + 1, "type": "pdf_page"}
        ))
    return out

def load_text(path: str) -> List[DocChunk]:
    basename = os.path.basename(path)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().strip()
    if not text:
        return []
    return [DocChunk(text=text, meta={"source": basename, "page": None, "type": "text"})]

def load_documents(raw_dir: str) -> List[DocChunk]:
    chunks: List[DocChunk] = []
    for filename in os.listdir(raw_dir):
        p = os.path.join(raw_dir, filename)
        if not os.path.isfile(p):
            continue
        lower = filename.lower()
        if lower.endswith(".pdf"):
            chunks.extend(load_pdf(p))
        elif lower.endswith(".txt") or lower.endswith(".md"):
            chunks.extend(load_text(p))
        # you can add .docx etc if needed
    return chunks
