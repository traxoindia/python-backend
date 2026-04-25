from datetime import datetime
from app.utils.hash import verify_password
from app.db.database import db
from app.utils.jwt import create_token
from app.services.email_service import send_email
from app.utils.vendor_Code_Creation import generate_vendor_code


vendor_collection = db["vendors"]


def generate_vendor_id():
    count = vendor_collection.count_documents({})
    return f"VEND{1000 + count + 1}"


def create_vendor(data: dict):
    vendor_id = generate_vendor_id()

    vendor_data = {
        "vendor_id": vendor_id,
        "company_details": data["company_details"],
        "contact_details": data["contact_details"],
        "location_details": data["location_details"],
        "financial_details": data["financial_details"],
        "online_presence": data.get("online_presence"),
        "status": "PENDING",  # important for approval flow
        "vendor_code":"",
        "code_sent": False,
        "created_at": datetime.utcnow()
    }

    result = vendor_collection.insert_one(vendor_data)
    vendor_data["_id"] = str(result.inserted_id)

    return vendor_data


def get_all_vendors():
    vendors = list(vendor_collection.find())
    for v in vendors:
        v["_id"] = str(v["_id"])
    return vendors

from datetime import datetime

PENDING = "PENDING"
APPROVED = "APPROVED"
REJECTED = "REJECTED"


def get_pending_vendors():
    vendors = list(vendor_collection.find({"status": PENDING}))
    for v in vendors:
        v["_id"] = str(v["_id"])
    return vendors


def approve_vendor(vendor_id: str, admin_id: str = "admin"):
    vendor = vendor_collection.find_one({"vendor_id": vendor_id})

    if not vendor:
        return {"error": "Vendor not found"}

    if vendor["status"] == APPROVED:
        return {"message": "Vendor already approved"}

    if vendor["status"] == REJECTED:
        return {"error": "Rejected vendor cannot be approved directly"}

    vendor_collection.update_one(
        {"vendor_id": vendor_id},
        {"$set": {
            "status": APPROVED,
            "approved_at": datetime.utcnow(),
            "approved_by": admin_id
        }}
    )

    return {"message": "Vendor approved successfully"}

def reject_vendor(vendor_id: str, reason: str = "Not specified", admin_id: str = "admin"):
    vendor = vendor_collection.find_one({"vendor_id": vendor_id})

    if not vendor:
        return {"error": "Vendor not found"}

    if vendor["status"] == REJECTED:
        return {"message": "Vendor already rejected"}

    vendor_collection.update_one(
        {"vendor_id": vendor_id},
        {"$set": {
            "status": REJECTED,
            "rejected_at": datetime.utcnow(),
            "rejected_by": admin_id,
            "rejection_reason": reason
        }}
    )

    return {"message": "Vendor rejected successfully"}




async def login_vendor(data):
    vendor = vendor_collection.find_one({
        "contact_details.email": data.email
    })

    if not vendor:
        return {"error": "Vendor not found"}

    if vendor.get("status") != "APPROVED":
        return {"error": "Vendor not approved by admin"}

    if data.password != vendor['contact_details']['phone_number']:
        return {"error": "Invalid password"}

    # ✅ Create token
    token = create_token({
        "id": str(vendor["_id"]),
        "email": vendor["contact_details"]["email"],
        "vendor_id": vendor["vendor_id"]
    })

    # ✅ SEND EMAIL ONLY ONCE
    if not vendor.get("code_sent", False):
        email = vendor["contact_details"]["email"]
        # vendor_code = vendor.get("vendor_code", "TIAPL/SC/001")  # fallback

        vendor_code = generate_vendor_code()

        await send_email(
            email,
            vendor_code
        )

        # ✅ Update DB
        vendor_collection.update_one(
           {"_id": vendor["_id"]},
           {
              "$set": {
                 "code_sent": True,
                 "vendor_code": vendor_code   # ✅ store code here
               }
            }
    )

    return {
        "token": token,
        "vendor_id": vendor["vendor_id"],
        "email": vendor["contact_details"]["email"],
        "company_name": vendor["company_details"]["company_name"]
    }


from app.db.database import requirement_collection 
def vendorSee_AllRequerments():
    print("Hello from service")
    
    requi_cursor = requirement_collection.find()
    requi_list = list(requi_cursor)

    if not requi_list:
        return {"error": "No requirements found"}

    # Convert ObjectId to string
    for item in requi_list:
        item["_id"] = str(item["_id"])

    return requi_list

