from sqlalchemy import text
from backend.database import engine, Base
# We import models so the 'Base' registry knows they exist
from backend.columns import Document, Chunk 

def init_db():
    print("🚀 Starting Database Initialization...")
    
    try:
        # Using a connection to enable the extension
        with engine.connect() as conn:
            print("  -> Enabling pgvector extension...")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()

            print("  -> Creating tables (Documents and Chunks)...")
            # Base looks at all classes inheriting from it (Document, Chunk)
            Base.metadata.create_all(bind=engine)
            
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    init_db()