from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    name: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
