import fitz
from .schemas import DocumentCreate 
from .columns import Document, Chunk
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastembed import TextEmbedding
from fastapi import HTTPException, Header

embed_model = TextEmbedding("BAAI/bge-base-en-v1.5")
#semantic_chunker = SemanticChunker(embed_model, breakpoint_threshold_type='percentile')
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    length_function = len,
    chunk_overlap = 100
)

def extract_text(file_bytes: bytes):
    text = []
    with fitz.open(stream=file_bytes, filetype='pdf') as doc:
        for page in doc:
            text.append(page.get_text())
    return ''.join(text)

def chunk_text(file_bytes: bytes, filename: str, db: Session):
    try:
    # Implement pdf reader and chunking
        raw_text = extract_text(file_bytes)
        new_doc = Document(filename = filename)
        
        db.add(new_doc)
        print(f'Document {filename} added to database')
        db.flush()
        
        chunks = recursive_splitter.split_text(raw_text)
        embeddings = embed_model.embed(chunks)
        print('Embedding generated...')
        for content, embedding in zip(chunks, embeddings):
            new_chunk = Chunk(
                document_id = new_doc.id,
                content = content,
                embedding = embedding.tolist()
            )
            db.add(new_chunk)
        print('Document was successfully chunked...')
        db.commit()
        print('Success! Chunks saved successfully in database')

    except Exception as e:
        db.rollback()
        print(f'Error! Transaction failed, rolling back changes {e}')


# def process_pdf_ingestion(file_bytes: bytes, filename: str, db: Session, content_type: str):
#     if content_type != "application/pdf":
#         raise HTTPException(
#             status_code=400, 
#             detail=f"File {filename} is not a PDF. Please upload a valid PDF."
#         )
#     MAX_SIZE = 50_000_000
#     if len(file_bytes) > MAX_SIZE:
#         raise HTTPException(status_code=413, detail="File too large")

#     try:
#         doc = fitz.open(stream=file_bytes, filetype="pdf")
#     except Exception:
#         raise HTTPException(status_code=400, detail="PDF is corrupted or invalid.")
#     to_save = []

#     for page in doc:
#         text = page.get_text()
#         if not text.strip():
#             continue

#         chunks = semantic_chunker.create_documents([text])

#         for chunk in chunks:
#             # 3. Generate Embedding (The "Vector" part!)
#             # FastEmbed returns a generator, we take the first item
#             vectors = embed_model.embed_documents([chunk.page_content])
#             vector = vectors[0] # Get the first (and only) vector

#             # 4. Prepare Database Object
#             db_chunk = Document(
#                 filename=filename,
#                 content=chunk.page_content,
#                 page_number=page.number + 1,
#                 embedding=vector
#             )
#             to_save.append(db_chunk)

#     db.add_all(to_save)
#     db.commit()
#     return len(to_save)