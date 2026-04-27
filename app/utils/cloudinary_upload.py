# import cloudinary.uploader
# import uuid
# from app.utils.cloudinary_config import cloudinary


# def upload_file(file, folder="Vendors"):
#     try:
#         public_id = f"{folder}/{uuid.uuid4()}"
#         extension = file.filename.split(".")[-1] if "." in file.filename else "pdf"
#         result = cloudinary.uploader.upload(
#             file.file,
#             public_id=public_id,
#             # resource_type="auto"  # supports PDF, images, docs
#             resource_type="raw",   # ✅ FIX HERE
#             format=extension,          # ✅ keep .pdf extension
#             use_filename=True
#         )

#         return result["secure_url"]

#     except Exception as e:
#         print("Cloudinary Upload Error:", e)
#         return None

import cloudinary.uploader
import uuid

def upload_file(file, folder="Vendors"):
    try:
        public_id = f"{folder}/{uuid.uuid4()}"

        result = cloudinary.uploader.upload(
            file.file,
            public_id=public_id,
            resource_type="auto"
        )

        return result["secure_url"]

    except Exception as e:
        print("Cloudinary Upload Error:", e)
        return None