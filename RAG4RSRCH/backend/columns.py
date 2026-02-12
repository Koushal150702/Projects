from sqlalchemy import (
    Integer, String, Text, ARRAY, Float, DateTime, Any
)
from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import datetime as dt
import sqlalchemy as sa

class Document(Base):
    __tablename__='documents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    upload_date: Mapped[dt.datetime] = mapped_column(DateTime, server_default=sa.func.now())
    chunks = relationship('Chunk', back_populates='document', cascade = 'all, delete-orphan')

class Chunk(Base):
    __tablename__ = 'chunks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id', ondelete='CASCADE'))
    document = relationship('Document', back_populates='chunks')
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Any] = mapped_column(Vector(768), nullable=False)

class Query(Base):
    __tablename__ = 'queries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Any] = mapped_column(Vector(768), nullable=False)
    
    # content: Mapped[str] = mapped_column(Text, nullable=False)
    # page_number: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # # We store the vector as an array of floats
    # # For 'BAAI/bge-base-en-v1.5', this will be a list of 768 numbers
    # embedding: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=True)
