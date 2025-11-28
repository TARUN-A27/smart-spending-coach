from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.auth import Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# --------------------------
# REGISTER (RAW SQL)
# --------------------------
@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):

    # Check if email exists
    result = db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": payload.email},
    ).fetchone()

    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_pw = hash_password(payload.password)

    # Insert user
    db.execute(
        text(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (:name, :email, :password_hash)
            """
        ),
        {
            "name": payload.name,
            "email": payload.email,
            "password_hash": hashed_pw,
        },
    )
    db.commit()

    # Fetch the created user
    created = db.execute(
        text(
            """
            SELECT id, name, email
            FROM users
            WHERE email = :email
            """
        ),
        {"email": payload.email},
    ).fetchone()

    return {
        "id": created.id,
        "name": created.name,
        "email": created.email,
    }


# --------------------------
# LOGIN (RAW SQL)
# --------------------------
@router.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    # Fetch user by email
    db_user = db.execute(
        text(
            """
            SELECT id, password_hash
            FROM users
            WHERE email = :email
            """
        ),
        {"email": payload.email},
    ).fetchone()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    # Verify password against password_hash
    if not verify_password(payload.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    # Create JWT access token (use "sub" because get_current_user reads that)
    token = create_access_token({"sub": str(db_user.id)})

    # Check whether profile exists
    profile = db.execute(
        text("SELECT id FROM user_profile WHERE user_id = :uid"),
        {"uid": db_user.id},
    ).fetchone()

    has_filled_profile = profile is not None

    return {
        "access_token": token,
        "token_type": "bearer",
        "has_filled_profile": has_filled_profile,
    }
