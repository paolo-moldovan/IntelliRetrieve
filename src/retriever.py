from typing import List
from .database.vector_db import VectorDB
from .config import settings
from .utils.logger import setup_logger
from .ranker import Ranker

logger = setup_logger(__name__)

class Retriever:
    def __init__(self, 
                 top_k: int = settings.TOP_K_RESULTS,
                 semantic_weight: float = settings.SEMANTIC_WEIGHT,
                 lexical_weight: float = settings.LEXICAL_WEIGHT):
        self.vector_db = VectorDB()
        self.top_k = top_k
        self.ranker = Ranker(
            semantic_weight=semantic_weight,
            lexical_weight=lexical_weight
        )
    
    def retrieve(self, query: str) -> List[str]:
        try:
            # Get initial candidates from vector DB
            results = self.vector_db.query(query, n_results=self.top_k * 2)
            
            # Re-rank documents
            ranked_docs = self.ranker.rank(query, results)
            
            # Return top-k after re-ranking
            return [doc["text"] for doc in ranked_docs[:self.top_k]]
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
