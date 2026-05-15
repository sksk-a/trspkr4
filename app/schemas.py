from typing import Optional

from pydantic import BaseModel, EmailStr, Field, conint, constr


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: list | dict | None = None


class ProductCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    count: int = Field(ge=0)
    description: str = Field(min_length=1, max_length=255)


class ProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True


class ValidatedUser(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    age: int
