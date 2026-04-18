from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CompanyDetails(BaseModel):
    company_name: str
    business_type: str  # Manufacturer / Supplier / Distributor
    gst_number: str
    pan_number: str
    certifications: Optional[str]


class ContactDetails(BaseModel):
    contact_person_name: str
    email: EmailStr
    phone_number: str
    alternate_phone_number: Optional[str]


class LocationDetails(BaseModel):
    address: str
    city: str
    state: str
    country: str
    pin_code: str


class FinancialDetails(BaseModel):
    payment_terms: str
    bank_account_details: str


class OnlinePresence(BaseModel):
    website: Optional[str]


class VendorCreate(BaseModel):
    company_details: CompanyDetails
    contact_details: ContactDetails
    location_details: LocationDetails
    financial_details: FinancialDetails
    online_presence: Optional[OnlinePresence]


class VendorResponse(VendorCreate):
    vendor_id: str
    status: str
    created_at: datetime

from pydantic import BaseModel
from typing import Optional


class VendorRejectRequest(BaseModel):
    reason: Optional[str] = "Not specified"    



class VendorLogin(BaseModel):
    email: str
    password: str