from fastapi import APIRouter, HTTPException, Depends
from app.schemas.vendor_schema import VendorCreate , VendorRejectRequest ,VendorLogin
# from app.services.vendor_service import create_vendor, get_all_vendors , approve_vendor , reject_vendor , get_pending_vendors , login_vendor
from app.services.vendor_service import (
    create_vendor,
    get_all_vendors,
    approve_vendor,
    reject_vendor,
    get_pending_vendors,
    login_vendor,
    vendorSee_AllRequerments
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/register")
def register_vendor(vendor: VendorCreate):
    return create_vendor(vendor.dict())


@router.get("/")
def list_vendors():
    return get_all_vendors()



@router.get("/pending")
def pending_vendors():
    return get_pending_vendors()

@router.put("/approve/{vendor_id}")
def approve(vendor_id: str):
    result = approve_vendor(vendor_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result

@router.put("/reject/{vendor_id}")
def reject(vendor_id: str, payload: VendorRejectRequest):
    result = reject_vendor(vendor_id, payload.reason)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
    return result


@router.post("/vendor-login")
def vendor_Login(data:VendorLogin):
    return login_vendor(data)


from app.services.vendor_service import vendorSee_AllRequerments
@router.get("/vendor-see-requirements")
def vendorSee_Allrequirements(current_user=Depends(get_current_user)):
    return vendorSee_AllRequerments()





from bson import ObjectId
from app.db.database import requirement_collection
@router.put("/approve-requirement/{requirement_id}")
def vendorApprove_Requirement(requirement_id: str, current_user=Depends(get_current_user)):
    requirement = requirement_collection.find_one({"_id": ObjectId(requirement_id)})


    if not requirement:
        return {"error": "Requirement not found"}

    if requirement["status"] != "open":
        return {"error": "Requirement is not open for approval"}
    
    # print(current_user)

    # ✅ Prevent duplicate + add vendor
    requirement_collection.update_one(
        {"_id": ObjectId(requirement_id)},
        {"$addToSet": {"ApproveVendor_ids": current_user["vendor_id"]}}
    )

    return {"message": "Requirement approved successfully by vendor"}
