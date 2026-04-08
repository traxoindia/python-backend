# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.models.branch_model import Branch

# router = APIRouter(prefix="/branches", tags=["Branches"])

# @router.post("/")
# def create_branch(name: str, location: str, company_id: int, db: Session = Depends(get_db)):
#     branch = Branch(name=name, location=location, company_id=company_id)
#     db.add(branch)
#     db.commit()
#     db.refresh(branch)
#     return branch

# @router.get("/")
# def get_branches(db: Session = Depends(get_db)):
#     return db.query(Branch).all()

# @router.delete("/{branch_id}")
# def delete_branch(branch_id: int, db: Session = Depends(get_db)):
#     branch = db.query(Branch).filter(Branch.id == branch_id).first()
    
#     if not branch:
#         return {"error": "Branch not found"}
    
#     db.delete(branch)
#     db.commit()
#     return {"message": "Deleted"}



from fastapi import APIRouter
from app.db.database import db
from bson import ObjectId

router = APIRouter(prefix="/branches", tags=["Branches"])


# CREATE BRANCH
@router.post("/")
def create_branch(name: str, location: str, company_id: str):
    branch = {
        "name": name,
        "location": location,
        "company_id": company_id
    }

    result = db["branches"].insert_one(branch)
    branch["_id"] = str(result.inserted_id)

    return branch


# GET ALL BRANCHES
@router.get("/")
def get_branches():
    branches = []

    for branch in db["branches"].find():
        branch["_id"] = str(branch["_id"])
        branches.append(branch)

    return branches


# DELETE BRANCH
@router.delete("/{branch_id}")
def delete_branch(branch_id: str):
    result = db["branches"].delete_one({"_id": ObjectId(branch_id)})

    if result.deleted_count == 0:
        return {"error": "Branch not found"}

    return {"message": "Deleted successfully"}
