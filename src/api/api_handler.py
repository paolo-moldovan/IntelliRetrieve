from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..indexer import Indexer
from ..query_processor import QueryProcessor
from ..config import settings

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    context_window: Optional[int] = 2000
    model: Optional[str] = "phi4"
    
class IndexRequest(BaseModel):
    file_paths: List[str]
    chunk_size: Optional[int] = 500
    chunk_overlap: Optional[int] = 50

@app.post("/query")
async def process_query(request: QueryRequest):
    try:
        processor = QueryProcessor(model=request.model)
        result = processor.process_query(
            query=request.query,
            context_window=request.context_window
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index")
async def index_documents(request: IndexRequest):
    try:
        indexer = Indexer(
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        indexer.index_documents(request.file_paths)
        return {"status": "success", "message": "Documents indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
