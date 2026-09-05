from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schemas import UserCreate, UserLogin
from app.models.user import User
from app.database.database import get_db
from app.security import hash_password, verify_password

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
            status_code = 400,
            content = {"message": "Имя пользователя должно быть не менее 3 символов!"},
            media_type = "application/json;charset=utf-8"
        )
    
    if len (user.password) < 8:
        return JSONResponse(
            status_code = 400,
            content = {"message": "Пароль должен быть не менее 8 символов!"},
            media_type = "application/json;charset=utf-8"
        )

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return JSONResponse(
            status_code = 400,
            content={"message": "Это имя пользователя уже занято!"},
            media_type="application/json;charset=utf-8"
        )
    
    hashed_password = hash_password(user.password)
    new_user = User(
        username = user.username,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return{
        "message": "Пользователь успешно зарегистрирован!",
        "id": new_user.id,
        "username": new_user.username
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return JSONResponse(
            status_code=401,
            content={"message": "Неверный логин или пароль!"},
            media_type="application/json;charset=utf-8"
        )

    return {
        "message": "Вход выполнен!",
        "id": db_user.id,
        "username": db_user.username
    }
