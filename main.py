import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from pymilvus import connections, utility, Collection
from sentence_transformers import SentenceTransformer
import uvicorn

# --- Configuration ---
_MILVUS_URI = os.getenv("MILVUS_URI", "./milvus_arabic_books.db")  # Using Milvus Lite (embedded) - PRODUCTION DATABASE
_COLLECTION_NAME = "arabic_books"  # PRODUCTION COLLECTION
_MODEL_NAME = "intfloat/multilingual-e5-large"

# --- Global Objects ---
model: Optional[SentenceTransformer] = None
collection: Optional[Collection] = None

# --- FastAPI Application ---
app = FastAPI(
    title="Filterable Arabic Books RAG API",
    version="1.1.0",
)

# Enable CORS for internet access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# --- Pydantic Models for API I/O ---
class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query in Arabic.", example="أبو هريرة سنة الوفاة")
    top_n: int = Field(3, gt=0, le=20, description="The number of results to return.")
    filter_books: Optional[List[str]] = Field(None, description="Optional list of book names to search within.", example=["book_folder_1", "book_folder_2"])

class SearchResult(BaseModel):
    score: float
    book_name: str
    file_path: str
    chunk_index: int
    text: str
    
    class Config:
        from_attributes = True

# --- API Events ---
@app.on_event("startup")
async def startup_event():
    global model, collection
    print("--- Server starting up ---")
    print(f"Connecting to Milvus Lite at: {_MILVUS_URI}")
    model = SentenceTransformer(_MODEL_NAME, trust_remote_code=True)
    connections.connect("default", uri=_MILVUS_URI)
    if not utility.has_collection(_COLLECTION_NAME):
        raise RuntimeError(f"Collection '{_COLLECTION_NAME}' not found.")
    collection = Collection(_COLLECTION_NAME)
    collection.load()
    print("--- Server is ready ---")

# --- API Endpoints ---
@app.get("/", summary="Health Check")
def read_root():
    return {"status": "ok"}

@app.post("/search", response_model=List[SearchResult], summary="Perform a semantic search with optional filtering")
async def search(request: SearchRequest = Body(...)):
    """
    Performs semantic search. If `filter_books` is provided, the search is restricted to those books.
    """
    if not collection or not model:
        raise HTTPException(status_code=503, detail="Server not fully initialized.")
        
    try:
        # 1. Generate query embedding
        prefixed_query = f"query: {request.query}"
        query_embedding = model.encode(prefixed_query)
        
        # 2. Construct filter expression (the key new feature)
        filter_expr = ""
        if request.filter_books:
            # Milvus's 'in' operator requires a list in this string format.
            filter_expr = f"book_name in {request.filter_books}"
            print(f"Applying filter: {filter_expr}")
        
        # 3. Define search parameters
        search_params = {"metric_type": "L2", "params": {"nprobe": 16}}
        
        # 4. Perform the search in Milvus
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=request.top_n,
            expr=filter_expr, # Apply the filter here
            output_fields=["book_name", "file_path", "chunk_text", "chunk_index"]
        )
        
        # 5. Format results
        response_data = []
        for hit in results[0]:
            entity_data = hit.entity.to_dict()['entity']
            # Map chunk_text to text for the response model
            response_data.append(SearchResult(
                score=hit.distance,
                book_name=entity_data['book_name'],
                file_path=entity_data['file_path'],
                chunk_index=entity_data['chunk_index'],
                text=entity_data['chunk_text']
            ))
        
        return response_data
    except Exception as e:
        print(f"An error occurred during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

