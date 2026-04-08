from pydantic import BaseModel

class BranchCreate(BaseModel):
    name: str
    location: str

class BranchResponse(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        orm_mode = True
        