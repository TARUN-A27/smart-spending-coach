# app/api/v1/routes_profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db
from app.core.security import get_current_user
from app.db.orm_models import User


router = APIRouter(prefix="/user", tags=["User Profile"])


@router.post("/profile")
def save_profile(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Save onboarding profile for the logged-in user.
    Frontend sends:
    {
      "role": "student" | "employee",
      "income": 10000,
      "age": 21,
      "financial_goal": "...",
      "expense_category": "...",
      "budgeting": "..."
    }
    """

    # Basic payload validation to avoid KeyError -> 500
    required_keys = [
        "role",
        "income",
        "age",
        "financial_goal",
        "expense_category",
        "budgeting",
    ]
    for key in required_keys:
        if key not in data:
            raise HTTPException(
                status_code=422,
                detail=f"Missing field: {key}",
            )

    # Check if profile already exists for this user
    existing = db.execute(
        text("SELECT id FROM user_profile WHERE user_id = :uid"),
        {"uid": current_user.id},
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Profile already submitted",
        )

    # Insert new profile
    db.execute(
        text(
            """
            INSERT INTO user_profile (
                user_id, role, income, age, financial_goal,
                expense_category, budgeting
            )
            VALUES (:uid, :role, :income, :age, :goal,
                    :category, :budgeting)
            """
        ),
        {
            "uid": current_user.id,
            "role": data["role"],
            "income": data["income"],
            "age": data["age"],
            "goal": data["financial_goal"],
            "category": data["expense_category"],
            "budgeting": data["budgeting"],
        },
    )

    db.commit()
    return {"message": "Profile saved successfully"}
