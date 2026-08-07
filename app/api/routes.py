from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schemas import UserCreate
from app.models.user import User
from app.database.database import get_db

router = APIRouter()

@router.get("/")
def root():
    return JSONResponse(
        content = {"message": "fastapi запущен!"},
        media_type = "application/json;charset=utf-8"
    )

@router.post("/register")
def register(user:UserCreate, db: Session = Depends(get_db)):

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

    new_user = User(
        username = user.username,
        password = user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return{
        "message": "Пользователь успешно зарегистрирован!",
        "id": new_user.id,
        "username": new_user.username
    }
