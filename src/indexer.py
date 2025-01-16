from typing import List, Union
from pathlib import Path

from .data_loader import DataLoader
from .chunker import Chunker
from .database.vector_db import VectorDB
from .utils.logger import setup_logger

logger = setup_logger(__name__)

class Indexer:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.data_loader = DataLoader()
        self.chunker = Chunker(chunk_size, chunk_overlap)
        self.vector_db = VectorDB()
        
    def index_documents(self, file_paths: List[Union[str, Path]]):
        for file_path in file_paths:
            try:
                content = self.data_loader.load_document(file_path)
                chunks = self.chunker.create_chunks(content)
                metadata = [{"source": str(file_path)} for _ in chunks]
                self.vector_db.add_documents(chunks, metadata)
                
                logger.info(f"Successfully indexed {file_path}")
            except Exception as e:
                logger.error(f"Error indexing {file_path}: {str(e)}")
                raise
