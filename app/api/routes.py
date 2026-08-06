from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas import Usercreate

router = APIRouter()

@router.get("/")
def root():
    return JSONResponse(
        content = {"message": "fastapi запущен!"},
        media_type = "application/json;charset=utf-8"
    )

@router.post("/register")
def register(user:Usercreate):
    return{
        "username": user.username,
        "password": user.password
    }
