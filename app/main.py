from itertools import count
from threading import Lock

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.exceptions import CustomExceptionA, CustomExceptionB
from app.models import Product
from app.schemas import ErrorResponse, ProductCreate, ProductOut, UserIn, UserOut, ValidatedUser

app = FastAPI(title="КР4", version="1.0.0")

Base.metadata.create_all(bind=engine)

users_db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()


def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


def reset_users_state() -> None:
    global _id_seq
    users_db.clear()
    _id_seq = count(start=1)


@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request, exc: CustomExceptionA):
    print(f"CustomExceptionA: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error_code=exc.error_code, message=exc.message).model_dump(),
    )


@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request, exc: CustomExceptionB):
    print(f"CustomExceptionB: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error_code=exc.error_code, message=exc.message).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    print(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            details=exc.errors(),
        ).model_dump(),
    )


@app.get("/")
def root():
    return {"message": "FastAPI запущен и работает!"}


@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise CustomExceptionB(f"Product with id={product_id} not found")
    return product


@app.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/errors/check-age/{age}")
def check_age(age: int):
    if age < 18:
        raise CustomExceptionA("Age must be at least 18")
    return {"message": "Age is valid"}


@app.get("/errors/resource/{resource_id}")
def read_fake_resource(resource_id: int):
    if resource_id != 1:
        raise CustomExceptionB("Fake resource not found")
    return {"id": 1, "name": "Existing resource"}


@app.post("/validate-user")
def validate_user(user: ValidatedUser):
    return {"message": "User data is valid", "user": user.model_dump()}


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    user_id = next_user_id()
    users_db[user_id] = user.model_dump()
    return {"id": user_id, **users_db[user_id]}


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **users_db[user_id]}


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if users_db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
