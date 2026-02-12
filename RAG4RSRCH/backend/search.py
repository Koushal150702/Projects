from fastembed import TextEmbedding
from .columns import Document, Chunk, Query
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select
from pgvector.sqlalchemy import Vector


embed_model = TextEmbedding('BAAI/bge-base-en-v1.5')

def search(query: str, db: Session):
    query_embedding = list(embed_model.embed([query]))[0]
    new_query = Query(
        content = query,
        embedding = query_embedding.tolist()
    )
    db.add(new_query)

    results = db.scalars(
        select(Chunk)
        .order_by(Chunk.embedding.cosine_distance(query_embedding.tolist()))
        .limit(5)
    ).all()
    print(f'\n{new_query.content}\n')
    db.commit()
    return results

