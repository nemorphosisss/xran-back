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

    if len (user.username) < 3:
        return JSONResponse(
            content = {"message": "Имя пользователя должно быть не менее 3 символов!"},
            media_type = "application/json;charset=utf-8"
        )
    
    if len (user.password) < 8:
        return JSONResponse(
            content = {"message": "Пароль должен быть не менее 8 символов!"},
            media_type = "application/json;charset=utf-8"
        )

    return{
        "username": "Пользователь авторизован",
        "password": user.password
    }
