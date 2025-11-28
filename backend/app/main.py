from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.db.database import Base, engine
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_profile import router as profile_router

# -------------------------
# DB SETUP
# -------------------------
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="Smart Spending Coach API", version="1.0.0")

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# FRONTEND PATHS
# -------------------------
FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../frontend")
)
PAGES_DIR = os.path.join(FRONTEND_DIR, "pages")

# -------------------------
# STATIC FILES
# -------------------------
# This matches how your HTML refers to:
#   /static/styles/reset.css
#   /static/styles/login.css
#   /static/assets/logo.png
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

# -------------------------
# PAGE ROUTES
# -------------------------


@app.get("/", include_in_schema=False)
def serve_root():
    return FileResponse(os.path.join(PAGES_DIR, "login.html"))


@app.get("/login.html", include_in_schema=False)
def serve_login():
    return FileResponse(os.path.join(PAGES_DIR, "login.html"))


@app.get("/questions.html", include_in_schema=False)
def serve_questions():
    return FileResponse(os.path.join(PAGES_DIR, "questions.html"))


@app.get("/dashboard.html", include_in_schema=False)
def serve_dashboard():
    return FileResponse(os.path.join(PAGES_DIR, "dashboard.html"))


# -------------------------
# API: BASIC PROFILE SUMMARY
# -------------------------
# This endpoint is what your dashboard.js is calling:
#   GET /user/profile/details
# You can later replace this stub with real DB logic.
@app.get("/user/profile/details")
async def get_user_profile_details():
    return {
        "name": "User",
        "monthly_income": 0,
        "top_expense_category": "-",
        "total_spend": 0,
        "net_savings": 0,
        "savings_rate": 0,
        "recommendations": [
            "Upload a bank statement to see your spending insights."
        ],
    }


# -------------------------
# API ROUTES
# -------------------------
app.include_router(auth_router)
app.include_router(profile_router)
