from pydantic import BaseModel
from typing import Optional, List

class DocumentBase(BaseModel):
    title: str
    content: str
    page_number: Optional[int] = None
    
class DocumentCreate(DocumentBase):
    pass

class DocumentOut(DocumentBase):
    id: int 
    class Config:
        from_attributes = True