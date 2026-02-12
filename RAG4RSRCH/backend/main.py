from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
import fitz #Pymupdf
from .schemas import DocumentCreate
from .database import Base, engine, SessionLocal, get_db
from .columns import Document
from sqlalchemy.orm import Session
from langchain_experimental.text_splitter import SemanticChunker
from .ingestion import chunk_text
from .search import search

app = FastAPI(title= 'RAG knowledge engine') # Create a fastapi app named app. Later app is the name used to run using uvicorn backend.app:app -reload

@app.get('/') # Create a health endpoint 
def health():
    return {'status' : 'ok'}


@app.get('/test_db') # test connection to db endpoint
def test_connection(db: Session = Depends(get_db)): 
    return {'message': 'Database session is active'}


@app.post('/upload')
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()

    chunk_text(
        file_bytes=file_bytes,
        filename=file.filename, 
        db=db
    )
    
    return {'message': 'PDF uploaded and chunked!'}
    
@app.post('/search')
def query_search(query: str, db: Session = Depends(get_db)):
    search(
        query, 
        db=db
    )

    return {'message' : 'Model response generated!'}
    
    # total_chunks = 0
    # file_content = file.file.read()
    # document = fitz.open(stream=file_content, filetype='pdf')
    # to_save = []
    # print('Document uploaded successfully')

    # for page in document:
    #     page_text = page.get_text()
    #     if not page_text.strip():
    #         continue
    #     chunks = semantic_chunker.create_documents([page_text])
    
    #     for chunk in chunks:
    #         db_chunk = Document(
    #             title = f'{file.filename}',
    #             content = chunk.page_content,
    #             page_number = page.number + 1
    #         )
    #         total_chunks+=1
    #         to_save.append(db_chunk)
    # db.add_all(to_save)        
    # db.commit()
    # print('Document table updated')

    # return {
    #     'filename' : file.filename, 
    #     'chunks_created': total_chunks,
    #     'status': 'Success! Text extracted'
    # }
