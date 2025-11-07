import os
import time
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from sentence_transformers import SentenceTransformer

# --- Configuration ---
_MILVUS_URI = "./milvus_arabic_books.db"  # Using Milvus Lite (embedded)
_COLLECTION_NAME = "arabic_books"
_DATA_PATH = "manhaj2030_books_cleaned_v1"
_MODEL_NAME = "intfloat/multilingual-e5-large"
_CHUNK_SIZE = 512
_CHUNK_OVERLAP = 64
_BATCH_SIZE = 100  # Process embeddings in batches to avoid memory issues

# --- Milvus Schema Definition ---
# The schema now includes 'book_name' which is essential for filtering.
field_pk = FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True)
field_embedding = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024)
field_book_name = FieldSchema(name="book_name", dtype=DataType.VARCHAR, max_length=256)
field_file_path = FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=512)
field_chunk_text = FieldSchema(name="chunk_text", dtype=DataType.VARCHAR, max_length=65535)
field_chunk_index = FieldSchema(name="chunk_index", dtype=DataType.INT64)

schema = CollectionSchema(
    fields=[field_pk, field_embedding, field_book_name, field_file_path, field_chunk_text, field_chunk_index],
    description="Collection for Arabic book chunks with metadata for filtering",
    enable_dynamic_field=False
)

def main():
    print("Starting ingestion process...")
    print(f"Connecting to Milvus Lite at: {_MILVUS_URI}")
    connections.connect("default", uri=_MILVUS_URI)
    
    if utility.has_collection(_COLLECTION_NAME):
        print(f"Dropping existing collection '{_COLLECTION_NAME}'.")
        utility.drop_collection(_COLLECTION_NAME)
    
    print(f"Creating collection '{_COLLECTION_NAME}'...")
    collection = Collection(name=_COLLECTION_NAME, schema=schema)
    print("Collection created.")
    
    print(f"Loading sentence transformer model: '{_MODEL_NAME}'")
    model = SentenceTransformer(_MODEL_NAME, trust_remote_code=True)
    print("Model loaded.")
    
    total_chunks_inserted = 0
    start_time = time.time()
    
    # Iterate through book folders. The folder name is treated as the book name.
    for book_folder in os.listdir(_DATA_PATH):
        book_path = os.path.join(_DATA_PATH, book_folder)
        if os.path.isdir(book_path):
            print(f"\nProcessing Book: {book_folder}")
            file_count = 0
            for filename in os.listdir(book_path):
                if filename.endswith(".txt"):
                    file_count += 1
                    file_path = os.path.join(book_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text = f.read()
                        
                        file_size_mb = len(text) / (1024 * 1024)
                        chunks = [text[i:i + _CHUNK_SIZE] for i in range(0, len(text), _CHUNK_SIZE - _CHUNK_OVERLAP)]
                        if not chunks: continue
                        
                        print(f"  - File {file_count}: {filename} ({file_size_mb:.2f} MB, {len(chunks)} chunks)")
                        
                        # Process chunks in batches to avoid memory issues
                        for batch_start in range(0, len(chunks), _BATCH_SIZE):
                            batch_end = min(batch_start + _BATCH_SIZE, len(chunks))
                            batch_chunks = chunks[batch_start:batch_end]
                            
                            prefixed_chunks = [f"passage: {chunk}" for chunk in batch_chunks]
                            embeddings = model.encode(prefixed_chunks, show_progress_bar=False)
                            
                            # Data to insert includes the book_folder as the 'book_name'
                            # Order must match schema: embedding, book_name, file_path, chunk_text, chunk_index
                            data_to_insert = [
                                embeddings.tolist(),
                                [book_folder] * len(batch_chunks),
                                [file_path] * len(batch_chunks),
                                batch_chunks,
                                list(range(batch_start, batch_end))
                            ]
                            
                            collection.insert(data_to_insert)
                            total_chunks_inserted += len(batch_chunks)
                            
                            if batch_end % (_BATCH_SIZE * 10) == 0 or batch_end == len(chunks):
                                print(f"    Progress: {batch_end}/{len(chunks)} chunks processed")
                        
                        print(f"    ✓ Completed {filename} ({len(chunks)} chunks)")
                    except Exception as e:
                        print(f"    ✗ ERROR processing file {file_path}: {e}")
    
    print("\nFlushing all data to database...")
    collection.flush()
    elapsed = time.time() - start_time
    print(f"Total chunks inserted: {total_chunks_inserted} (elapsed: {elapsed/60:.1f} minutes)")
    
    print("\nCreating index for the collection...")
    index_params = {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
    collection.create_index(field_name="embedding", index_params=index_params)
    utility.wait_for_index_building_complete(_COLLECTION_NAME)
    print("Index created successfully.")
    
    print("Loading collection into memory...")
    collection.load()
    print("Collection loaded into memory.")
    
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"✓ Ingestion Complete!")
    print(f"  Total chunks: {total_chunks_inserted}")
    print(f"  Total time: {total_time/60:.1f} minutes ({total_time:.2f} seconds)")
    print(f"  Average speed: {total_chunks_inserted/(total_time/60):.1f} chunks/minute")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

