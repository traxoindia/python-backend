from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Requirement(BaseModel):
    title: str
    description: str
    quantity: int
    category: str
    company_name: str
    status: str = "open"
    created_at: datetime = datetime.utcnow()