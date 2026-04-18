from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.company_routes import router as company_router
from app.routes import branch_routes
from app.routes import department_routes
from app.routes import vendor_routes 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(company_router)
app.include_router(branch_routes.router)
app.include_router(department_routes.router)
app.include_router(vendor_routes.router)

from app.routes import auth_routes   

app.include_router(auth_routes.router)

from app.routes.auth_routes import router as auth_router

app.include_router(auth_router)

from app.routes.procurement_routes import router as procurement_router
app.include_router(procurement_router)

@app.get("/")
def home():
    return {"message": "Admin Backend Running"}
