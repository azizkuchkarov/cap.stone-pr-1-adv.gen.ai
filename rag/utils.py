from typing import List, Tuple
from .loaders import DocChunk

def format_context(snips: List[Tuple[DocChunk, float]]) -> str:
    lines = []
    for c, score in snips:
        src = c.meta.get("source")
        page = c.meta.get("page", None)
        lines.append(
            f"- (score={score:.3f}) [{src}, page {page if page else 'N/A'}]\n  {c.text}"
        )
    return "\n".join(lines)

def is_answerable(snips: List[Tuple[DocChunk, float]], min_score: float) -> bool:
    if not snips:
        return False
    best = snips[0][1]
    return best >= min_score
