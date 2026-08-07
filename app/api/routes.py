from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas import UserCreate

router = APIRouter()

@router.get("/")
def root():
    return JSONResponse(
        content = {"message": "fastapi запущен!"},
        media_type = "application/json;charset=utf-8"
    )

@router.post("/register")
def register(user:UserCreate):
    return{
        "username": user.username,
        "password": user.password
    }
