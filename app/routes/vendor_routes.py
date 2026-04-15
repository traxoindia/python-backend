from fastapi import APIRouter
from app.schemas.vendor_schema import VendorCreate
from app.services.vendor_service import create_vendor, get_all_vendors

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/register")
def register_vendor(vendor: VendorCreate):
    return create_vendor(vendor.dict())


@router.get("/")
def list_vendors():
    return get_all_vendors()