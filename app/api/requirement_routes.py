from fastapi import APIRouter, Depends
from app.models.requirement_model import Requirement
from app.db.database import requirement_collection

router = APIRouter(prefix="/requirement", tags=["requirement"])

@router.post("/create-requirement")
def create_requirement(req: Requirement):
    requirement_collection.insert_one(req.dict())
    return {"message": "Requirement created successfully"}

@router.get("/vendor/requirements")
def get_all_requirements():
    requirements = list(requirement_collection.find({"status": "open"}))
    
    for r in requirements:
        r["_name"] = str(r["_name"])  # convert ObjectId
    
    return requirements

@router.get("/vendor/requirem" \
            "ents")


def get_requirements(category: str = None):
    query = {"status": "open"}
    
    if category:
        query["category"] = category

    requirements = list(requirement_collection.find(query))
    
    for r in requirements:
        r["_name"] = str(r["_name"])

    return requirements
