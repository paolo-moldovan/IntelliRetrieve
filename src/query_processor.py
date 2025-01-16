from typing import Dict, List
from .retriever import Retriever
from .generator import Generator
from .config import settings
from .utils.logger import setup_logger

logger = setup_logger(__name__)

class QueryProcessor:
    def __init__(self, model: str = settings.DEFAULT_MODEL):
        self.retriever = Retriever()
        self.generator = Generator(model=model)
    
    def process_query(self, query: str, context_window: int = settings.DEFAULT_CONTEXT_WINDOW) -> Dict:
        try:
            relevant_docs = self.retriever.retrieve(query)
            response = self.generator.generate(query, relevant_docs)
            
            return {
                "response": response,
                "context": relevant_docs
            }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
