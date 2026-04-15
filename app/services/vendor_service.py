from datetime import datetime
from bson import ObjectId
from app.db.database import db

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