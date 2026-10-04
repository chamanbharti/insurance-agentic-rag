from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LoadedDocument:
    source: str
    title: str
    document_type: str
    version: str
    content: str
    path: Path


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    content: str
