from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "phi4"
    
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    DEFAULT_CHUNK_SIZE: int = 500
    DEFAULT_CHUNK_OVERLAP: int = 50
    
    DEFAULT_CONTEXT_WINDOW: int = 2000
    TOP_K_RESULTS: int = 3
    
    # Ranking settings
    SEMANTIC_WEIGHT: float = 0.7
    LEXICAL_WEIGHT: float = 0.3
    RANKING_MODEL: str = "all-MiniLM-L6-v2"

settings = Settings() 