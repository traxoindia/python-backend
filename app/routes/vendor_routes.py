from fastapi import APIRouter, HTTPException
from app.schemas.vendor_schema import VendorCreate , VendorRejectRequest ,VendorLogin
from app.services.vendor_service import create_vendor, get_all_vendors , approve_vendor , reject_vendor , get_pending_vendors , login_vendor

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/register")
def register_vendor(vendor: VendorCreate):
    return create_vendor(vendor.dict())


@router.get("/")
def list_vendors():
    return get_all_vendors()


# from fastapi import APIRouter
# from app.schemas.vendor_schema import VendorRejectRequest

# from app.services.vendor_service import (
#     approve_vendor,
#     reject_vendor,
#     get_pending_vendors
# )

# router = APIRouter(prefix="/vendors", tags=["Vendors"])

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