from sqlalchemy import create_engine
from .config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.DB_URL,
    echo = True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# # sessionmaker is a class that helps us create a 'SessionLocal' class
# # autocommit=False: We want to manually decide when to save data
# # autoflush=False: We don't want it to send data to the DB until we are ready
# # bind=engine: This tells the factory which 'pipe' (engine) to use

