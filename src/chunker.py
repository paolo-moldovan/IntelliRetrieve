from typing import List
import nltk
from nltk.tokenize import sent_tokenize
from pathlib import Path
import os

class Chunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._ensure_nltk_data()

    def _ensure_nltk_data(self):
        try:
            sent_tokenize("Test sentence.")
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
            except Exception as e:
                nltk_data_dir = Path.home() / 'nltk_data'
                if not nltk_data_dir.exists():
                    nltk_data_dir.mkdir(parents=True, exist_ok=True)
                nltk.download('punkt', quiet=True)

    def create_chunks(self, text: str) -> List[str]:
        if not text.strip():
            return []
            
        try:
            sentences = sent_tokenize(text)
        except Exception as e:
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            if not sentences:
                return [text]

        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > self.chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                
                overlap_size = 0
                current_chunk = []
                
                for prev_sent in reversed(current_chunk):
                    if overlap_size + len(prev_sent) > self.chunk_overlap:
                        break
                    current_chunk.insert(0, prev_sent)
                    overlap_size += len(prev_sent)
                
                current_size = overlap_size
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks or [text]
